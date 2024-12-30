import copy
from enum import Enum
from collections import namedtuple
from waveforms import Waveform, wave_eval
from waveforms.math.signal import getFTMatrix, shift
import nsqdriver.nswave as nw

import numpy as np

try:
    import waveforms

    HAS_WAVEFORMS = True
except ImportError as e:
    HAS_WAVEFORMS = False

try:
    from .common import BaseDriver, Quantity, get_coef
except ImportError as e:

    class BaseDriver:

        def __init__(self, addr, timeout, **kw):
            self.addr = addr
            self.timeout = timeout


    class Quantity(object):

        def __init__(self, name: str, value=None, ch: int = 1, unit: str = ''):
            self.name = name
            self.default = dict(value=value, ch=ch, unit=unit)

    # def get_coef(*args):
    #     return '', '', '', ''

DEBUG_PRINT = False


def get_coef(coef_info, sampleRate):
    start, stop = coef_info['start'], coef_info['stop']
    numberOfPoints = int(
        (stop - start) * sampleRate)
    if numberOfPoints % 64 != 0:
        numberOfPoints = numberOfPoints + 64 - numberOfPoints % 64
    t = np.arange(numberOfPoints) / sampleRate + start

    fList = []
    wList = []
    phases = []

    for kw in coef_info['wList']:
        Delta, t0, weight, w, phase = kw['Delta'], kw['t0'], kw['weight'], kw['w'], kw['phase']
        fList.append(Delta)

        if w is not None:
            w = np.zeros(numberOfPoints, dtype=complex)
            w[:len(w)] = w
            w = shift(w, t0 - start)
            phases.append(np.mod(phase + 2 * np.pi * Delta * start, 2 * np.pi))
        else:
            weight = weight
            if isinstance(weight, np.ndarray):
                pass
            else:
                if isinstance(weight, str):
                    fun = wave_eval(weight) >> t0
                elif isinstance(weight, Waveform):
                    fun = weight >> t0
                else:
                    raise TypeError(f'Unsupported type {weight}')
                weight = fun(t)
            phase += 2 * np.pi * Delta * start
            w = getFTMatrix([Delta],
                            numberOfPoints,
                            phaseList=[phase],
                            weight=weight,
                            sampleRate=sampleRate)[:, 0]
            phases.append(np.mod(phase, 2 * np.pi))
        wList.append(w)
    return np.asarray(wList), fList, numberOfPoints, phases, round((stop - t0) * sampleRate), t


@nw.kernel
def program_cap(param: nw.Var):
    #
    nw.wait_for_trigger()
    i: nw.Var
    # param: [[100e-9, 1e-6], [200e-9, 1e-6]]
    for i in param:
        nw.wait(i[0])
        nw.capture(i[1], i[2], i[3])


ProbeSegment = namedtuple('ProbeSegment', ['start', 'stop', 'freq'])


CaptureCmd = namedtuple('CaptureCmd', [
    'start', 'ad_duration', 'delay', 'da_duration', 'freqs', 'delays'
])


class DemodulateMode(str, Enum):
    MORE_QUBIT = 'more_qubit'
    COMPLEX_SEQ = 'complex_seq'


class Driver(BaseDriver):
    CHs = list(range(1, 25))
    segment = ('ns', '111|112|113|114|115')
    res_map = []

    quants = [
        Quantity('ReInit', value={}, ch=1),  # set, 设备重新初始化
        Quantity('Instruction', value=None, ch=1),  # set   参数化波形指令队列配置
        # 采集运行参数
        Quantity('Shot', value=1024, ch=1),  # set,运行次数
        Quantity('PointNumber', value=16384, unit='point'),  # set/get,AD采样点数
        Quantity('TriggerDelay', value=0, ch=1, unit='s'),  # set/get,AD采样延时
        Quantity('FrequencyList', value=[], ch=1,
                 unit='Hz'),  # set/get,解调频率列表，list，单位Hz
        Quantity('PhaseList', value=[], ch=1,
                 unit='Hz'),  # set/get,解调频率列表，list，单位Hz
        Quantity('Coefficient', value=None, ch=1),
        Quantity('DemodulationParam', value=None, ch=1),
        Quantity('CaptureMode'),
        Quantity('StartCapture'),  # set,开启采集（执行前复位）
        Quantity('TraceIQ', ch=1),  # get,获取原始时域数据
        # 返回：array(shot, point)
        Quantity('IQ', ch=1),  # get,获取解调后数据,默认复数返回
        # 系统参数，宏定义修改，open时下发
        # 复数返回：array(shot,frequency)
        # 实数返回：array(IQ,shot,frequency)

        # 任意波形发生器
        Quantity('Waveform', value=np.array([]), ch=1),  # set/get,下发原始波形数据
        Quantity('Delay', value=0, ch=1),  # set/get,播放延时
        Quantity('KeepAmp', value=0
                 ),  # set, 电平是否维持在波形最后一个值, 0：波形播放完成后归0，1：保持波形最后一个值，2:保持波形第一个值
        Quantity('Biasing', value=0, ch=1),  # set, 播放延迟
        Quantity('LinSpace', value=[0, 30e-6, 1000],
                 ch=1),  # set/get, np.linspace函数，用于生成timeline
        Quantity('Output', value=True, ch=1),  # set/get,播放通道开关设置
        Quantity('GenWave', value=None,
                 ch=1),  # set/get, 设备接收waveform对象，根据waveform对象直接生成波形
        # set/get, 设备接收IQ分离的waveform对象列表，根据waveform对象列表直接生成波形
        Quantity('GenWaveIQ', value=None, ch=1),
        Quantity('MultiGenWave', value={1: np.ndarray([])}),  # 多通道波形同时下发
        Quantity('EnableWaveCache', value=False),  # 是否开启waveform缓存
        Quantity('PushWaveCache'),  # 使waveform缓存中的波形数据生效
        # 混频相关配置
        Quantity('EnableDAMixer', value=False, ch=1),  # DA通道混频模式开关
        Quantity('MixingWave', ),  # 修改完混频相关参数后，运行混频器
        Quantity('DAIQRate', value=1e9, ch=1),  # 基带信号采样率
        Quantity('DALOFreq', value=100e6, ch=1),  # 中频信号频率
        Quantity('DALOPhase', value=0, ch=1),  # 基带信号相位，弧度制
        Quantity('DASideband', value='lower', ch=1),  # 混频后取的边带
        Quantity('DAWindow', value=None, ch=1),
        # 基带信号升采样率时所使用的窗函数，默认不使用任何窗，
        # 可选：None、boxcar、triang、blackman、hamming、hann、bartlett、flattop、parzen、bohman、blackmanharris、nuttall、
        # barthann、cosine、exponential、tukey、taylor

        # 内触发
        Quantity('GenerateTrig', value=1e7,
                 unit='ns'),  # set/get,触发周期单位ns，触发数量=shot
        Quantity('UpdateFirmware', value='', ch=1),  # qsync固件更新
        Quantity('PipInstall')  # pip install in instance
    ]

    def __init__(self, addr: str = '', timeout: float = 10.0, **kw):
        super().__init__(addr, timeout=timeout, **kw)
        self.handle = None
        self.model = 'NS_MCI'  # 默认为设备名字
        self.srate = 8e9
        self.ad_srate = 4e9
        self.addr = addr
        self.timeout = timeout
        self.chs = set()  # 记录配置过的ch通道
        self.IQ_cache = {}
        self.coef_cache = {}
        self.res_maps = {}
        self.probe_da_wave = {}
        self.probe_delay = 32e-9
        self.capture_cmds: "dict[int, list[CaptureCmd]]" = {}
        self.capture_cali_param: "dict[int, np.ndarray]" = {}
        self.capture_points: "dict[int, np.ndarray]" = {}
        self.demodulate_mode = DemodulateMode.MORE_QUBIT

    def open(self, **kw):
        """
        输入IP打开设备，配置默认超时时间为5秒
        打开设备时配置RFSoC采样时钟，采样时钟以参数定义
        """
        from nsqdriver import MCIDriver

        DArate = 8e9
        ADrate = 4e9
        sysparam = {
            "MixMode": 2,
            "RefClock": "out",
            "DArate": DArate,
            "ADrate": ADrate,
            "CaptureMode": 0,
            "INMixMode": 2,  # 4～6 GHz 取 1， 6 ～ 8 GHz 取 2
        }
        sysparam.update(kw.get('system_parameter', {}))

        device = MCIDriver(self.addr, self.timeout)
        device.open(system_parameter=sysparam)
        self.handle = device

    def granularity4ns(self, delay):
        points_4ns = 16  # self.ad_srate*4e-6
        return delay*self.ad_srate//points_4ns*points_4ns/self.ad_srate

    @staticmethod
    def _delay2_phase(delay, freq):
        return 2*np.pi*freq*delay

    def get_sequence_in_time(self, coef_info: dict) -> list[CaptureCmd]:
        w_list = coef_info.get('wList', [])
        time_segments: "list[ProbeSegment]" = []

        for wave in w_list:
            t0 = wave['t0']
            weight_expr = wave['weight']

            # 假设 weight 表达式格式为 "square(X) >> Y"，我们提取实际时间宽度
            # duration = float(weight_expr.split('>>')[1].strip())
            _start, _stop, _ = wave_eval(weight_expr).bounds

            # 将区间加入列表
            seg = ProbeSegment(t0+_start, t0+_stop, wave['Delta'])
            time_segments.append(seg)

        # 按起始时间排序
        time_segments.sort()

        # 结果存储
        non_overlapping_segments: list[CaptureCmd] = []
        current_start, current_end = time_segments[0].start, time_segments[0].stop
        current_cmd = CaptureCmd(0, 0, 0, 0, [time_segments[0].freq], [0.])
        current_align_delay = current_start-self.granularity4ns(current_start)
        pointer = 0

        for seg in time_segments[1:]:
            if seg.start > current_end:
                # 如果不重叠，保存当前段并移动到下一段
                if pointer == 0:
                    current_cmd = current_cmd._replace(start=current_start - pointer)
                else:
                    current_cmd = current_cmd._replace(start=current_start - pointer - self.probe_delay)
                current_cmd = current_cmd._replace(ad_duration=current_end - current_start)
                current_cmd = current_cmd._replace(delay=self.probe_delay)
                current_cmd = current_cmd._replace(da_duration=current_end - current_start)
                non_overlapping_segments.append(current_cmd)

                current_cmd = CaptureCmd(0, 0, 0, 0, [seg.freq], [0.])
                pointer = current_end
                current_start, current_end = seg.start, seg.stop
            else:
                # 如果有重叠，扩展当前段
                current_end = max(current_end, seg.stop)
                current_cmd.freqs.append(seg.freq)
                # 由delay换算解缠绕相位
                current_cmd.delays.append(seg.start-current_start)
        else:
            # 添加最后一个段
            current_cmd = current_cmd._replace(start=current_start - pointer - self.probe_delay)
            current_cmd = current_cmd._replace(ad_duration=current_end - current_start)
            current_cmd = current_cmd._replace(delay=self.probe_delay)
            current_cmd = current_cmd._replace(da_duration=current_end - current_start)
            non_overlapping_segments.append(current_cmd)
        return non_overlapping_segments

    def generate_para(self, coef_info, ch):
        res_map = []
        phase_map = []
        points_map = []
        freq_map = []
        seq_param = []

        self.capture_cmds[ch] = seq = self.get_sequence_in_time(coef_info)

        for segment in seq:
            freq_map.extend(segment.freqs)
        freq_map = list(set(freq_map))

        for cap_num, segment in enumerate(seq):
            _start = self.granularity4ns(segment.start)
            _start_diff = segment.start-_start
            seq_param.append([
                _start, segment.ad_duration, segment.delay, segment.da_duration
            ])
            for delay, freq in zip(segment.delays, segment.freqs):
                res_map.append([freq_map.index(freq), cap_num])
                phase_map.append(self._delay2_phase(delay, freq))
                points_map.append(segment.ad_duration*self.ad_srate)

        self.res_maps[ch] = res_map
        self.capture_cali_param[ch] = np.exp(-1j*np.array(phase_map)).reshape((-1, 1))
        self.capture_points[ch] = np.array(points_map).reshape((-1, 1))
        return program_cap(seq_param), freq_map

    def get_coef_res(self, iq_res, ch):
        res = []
        for (freq_num, cap_num) in self.res_maps[ch]:
            res.append(iq_res[freq_num][cap_num::len(self.capture_cmds[ch])])
        # 采样点归一化
        res = np.array(res)/self.capture_points[ch]
        # 校准相位
        res *= self.capture_cali_param[ch]

        return res

    def close(self, **kw):
        """
        关闭设备
        """
        if getattr(self, 'handle', None) is not None:
            self.handle.close()
            self.handle = None

    def set(self, *args, **kwargs):
        return self.handle.set(*args, **kwargs)

    def get(self, *args, **kwargs):

        return self.handle.get(*args, **kwargs)

    def write(self, name: str, value, **kw):
        channel = kw.get('ch', 1)
        if name in {'Coefficient'}:
            # data, f_list, numberOfPoints, phases, points, _ = get_coef(value, 4e9)
            coef_info = value
            self.chs.add(channel)
            kernel, freq_map = self.generate_para(coef_info, channel)
            self.handle.set("Program", kernel, channel)
            self.handle.set("FreqList", freq_map, channel)
            self.handle.set("TimeWidth", 2e-6, channel)
            self.coef_cache.update({channel: coef_info})
        # elif name in {'Waveform'} and isinstance(value, waveforms.Waveform):
        #     self.probe_da_wave[channel] = value
        elif name in {
            'CaptureMode', 'SystemSync', 'ResetTrig', 'TrigPeriod',
            'TrigFrom'
        }:
            pass
        else:
            if name in {"Shot"}:
                self.shots = value
            return self.handle.set(name, value, channel)

    def read(self, name: str, **kw):
        channel = kw.get('ch', 1)
        if name in {"IQ"}:
            iq_res = self.handle.get(
                "IQ", channel, round(self.shots * len(self.capture_cmds[channel]))
            )

            result = self.get_coef_res(iq_res, channel).T
            if len(self.chs) != 0 and channel in self.chs:
                self.chs.remove(channel)
            # self.IQ_cache.update({channel: result})
            if len(self.chs) == 0:
                self.write("TerminateUpload", 1)  # 实验的开始必须加此句话
        else:
            result = self.handle.get(name, channel)
        return result


if __name__ == '__main__':
    co = {'start': 0.0, 'stop': 8.605e-06, 'wList': [
        {'Delta': 6796613333.333333, 'phase': -0.0, 'weight': 'square(8e-07) >> 4e-07', 'window': (0, 1024), 'w': None,
         't0': 1.5e-08, 'phi': 2.4311851282940524, 'threshold': 9.645718574523926},
        {'Delta': 6965129999.666667, 'phase': -0.0, 'weight': 'square(8e-07) >> 4e-07', 'window': (0, 1024), 'w': None,
         't0': 2.345e-06, 'phi': 2.1739656328752264, 'threshold': 20.36802101135254},
        {'Delta': 6866353333.333333, 'phase': -0.0, 'weight': 'square(8e-07) >> 4e-07', 'window': (0, 1024), 'w': None,
         't0': 2.345e-06, 'phi': 1.851749364542847, 'threshold': 21.65827751159668},
        {'Delta': 6796613333.333333, 'phase': -0.0, 'weight': 'square(8e-07) >> 4e-07', 'window': (0, 1024), 'w': None,
         't0': 5.175e-06, 'phi': 2.4311851282940524, 'threshold': 9.645718574523926},
        {'Delta': 6965129999.666667, 'phase': -0.0, 'weight': 'square(8e-07) >> 4e-07', 'window': (0, 1024), 'w': None,
         't0': 5.175e-06, 'phi': 2.1739656328752264, 'threshold': 20.36802101135254},
        {'Delta': 6866353333.333333, 'phase': -0.0, 'weight': 'square(8e-07) >> 4e-07', 'window': (0, 1024), 'w': None,
         't0': 5.175e-06, 'phi': 1.851749364542847, 'threshold': 21.65827751159668},
        {'Delta': 6796613333.333333, 'phase': -0.0, 'weight': 'square(8e-07) >> 4e-07', 'window': (0, 1024), 'w': None,
         't0': 7.805e-06, 'phi': 2.4311851282940524, 'threshold': 9.645718574523926},
        {'Delta': 6796613333.333333, 'phase': -0.0, 'weight': 'square(8e-07) >> 4e-07', 'window': (0, 1024), 'w': None,
         't0': 8.805e-06, 'phi': 2.4311851282940524, 'threshold': 9.645718574523926},
        {'Delta': 6965129999.666667, 'phase': -0.0, 'weight': 'square(8e-07) >> 4e-07', 'window': (0, 1024), 'w': None,
         't0': 9.005e-06, 'phi': 2.4311851282940524, 'threshold': 9.645718574523926}
    ]}
    _d = Driver('127.0.0.1', 300)
    res = _d.generate_para(co, 1)
