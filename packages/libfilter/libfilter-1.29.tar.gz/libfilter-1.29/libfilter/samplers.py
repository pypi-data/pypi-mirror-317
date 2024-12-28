from .audio_filters import *

class Decimator:
    """
    Decimates a list of samples of a selected sample rate to a another, tested in audacity, here's how it works:
    
    Input -> LPF (anti-aliasing) -> Decimator (take every ratio'th of the input list) -> Output
    """
    def __init__(self, ratio: int, sample_rate: float):
        self.sr = sample_rate
        self.nsr = sample_rate/ratio
        self.ratio = ratio
        self.lpf = MonoButterworthLPF(self.nsr, sample_rate)
    def process(self, audio: list) -> list:
        return [self.lpf.process(i) for i in audio][::self.ratio]
class Interpolator:
    """
    Makes more samples using linear interpolation, see how the Declipper works
    """
    def __init__(self, ratio: int, sample_rate: int):
        self.sr = sample_rate
        self.nsr = sample_rate*ratio
        self.ratio = ratio
    def process(self, audio: list) -> list:
        out = []
        padded_audio = [audio[0]] + audio + [audio[-1]]
        for past, now, future in zip(padded_audio, padded_audio[1:], padded_audio[2:]):
            out.append(now)
            for i in range(1, self.ratio):
                t = i / self.ratio  # Interpolation factor between 0 and 1
                interpolated = now * (1 - t) + future * t
                out.append(interpolated)
        return out