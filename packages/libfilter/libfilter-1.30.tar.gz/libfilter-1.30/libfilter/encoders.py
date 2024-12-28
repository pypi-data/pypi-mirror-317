from .base_classes import *
from .oscillators import *
from .audio_filters import *

class FMStereoEncoder(Encoder):
    """
    FM stereo encoder, can uses the MultiSine oscilator to generate 2 harmonics, one 38 khz 2nd 57 khz, for RDS
    """
    def __init__(self, sample_rate:float, output_57k: bool=False, volumes: list=[0.7, 0.1, 0.3, 1]):
        """
        volumes is a list with the volumes of each signals in this order: mono, pilot, stereo, mpx
        """
        if sample_rate < (53000*2) and not output_57k:
            raise Exception("Sample rate too small to stereo encode")
        elif sample_rate < (57000*2) and output_57k:
            raise Exception("Sample rate too small to stereo encode (and generate rds)")
        self.osc = MultiSine(19000, sample_rate, 2) # Multisine generates a number of harmonics of a signal, which are perfectly is phase and thus great for this purpose
        self.stm = StereoToMono()
        self.lpf = StereoButterworthLPF(15000, sample_rate)
        self.mono_vol, self.pilot_vol, self.stereo_vol, self.mpx_vol = volumes
        self.output_57k = output_57k
    def encode(self, left: float, right: float, mpx:float=0.0):
        left,right = self.lpf.process(left, right)
        
        pilot, stereo_carrier, rds_carrier = self.osc.process()
        
        mono = self.stm.process(left, right)
        stereo = (left-right)
        modulated_stereo = stereo*stereo_carrier # Can't use the DSB-SC mod object because it generates it's own sine wave
        
        out = 0.0
        out += (mono*self.mono_vol)
        out += (pilot*self.pilot_vol)
        out += (modulated_stereo*self.stereo_vol)
        out += (mpx*self.mpx_vol)
        
        if self.output_57k:
            return out, rds_carrier
        else:
            return out
class DiffrentialEncoder(Encoder):
    """
    Diffrential encoder, starts with 0, and every 1 is so it changed, so for example to encode 0b1100 you have it being 0b1010
    """
    def __init__(self, preamble:bool=False):
        self.last_bit = preamble
    def encode(self, signal: bool) -> bool:
        out = self.last_bit^signal # that also works on bools
        self.last_bit = signal
        return out