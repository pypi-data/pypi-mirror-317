from .base_classes import *
from .oscillators import *
from .audio_filters import *

class FMStereoEncoder(Encoder):
    """
    FM stereo encoder, can uses the MultiSine oscilator to generate 1 harmonics, 38 khz
    """
    def __init__(self, sample_rate:float, output_pilot: bool=False, volumes: list=[0.5, 0.1, 0.5, 1], lpf:float=15000, clipper_threshold:float=1.0):
        """
        volumes is a list with the volumes of each signals in this order: mono, pilot, stereo, mpx , also i redecommend to keep stereo same level as mono
        """
        if sample_rate < (53000*2):
            raise Exception("Sample rate too small to stereo encode (minimal is 106 KHz)")
        if lpf > 18500:
            raise ValueError("Are you high with that LPF? Just use the MPX input for god's sake!")
        if clipper_threshold > 1.0:
            raise Exception("Nuh uh")
        self.osc = MultiSine(19000, sample_rate, 1) # Multisine generates a number of harmonics of a signal, which are perfectly is phase and thus great for this purpose
        self.lpf = StereoButterworthLPF(lpf, sample_rate)
        self.clipper = StereoClipper(clipper_threshold)
        self.mono_vol, self.pilot_vol, self.stereo_vol, self.mpx_vol = volumes
        self.output_pilot = output_pilot
    def encode(self, left: float, right: float, mpx:float=0.0):
        left, right = self.lpf.process(left, right)
        left, right = self.clipper.process(left, right) # Clipper after LPF because clipper could distort signal too much for lpf
        
        pilot, stereo_carrier = self.osc.process()
        
        mono = (left+right)/2
        stereo = (left-right)/2
        modulated_stereo = stereo*stereo_carrier # Can't use the DSB-SC mod object because it generates it's own sine wave
        
        out = 0.0
        out += (mono*self.mono_vol)
        out += (pilot*self.pilot_vol)
        out += (modulated_stereo*self.stereo_vol)
        out += (mpx*self.mpx_vol)
        
        if self.output_pilot:
            return out, pilot
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