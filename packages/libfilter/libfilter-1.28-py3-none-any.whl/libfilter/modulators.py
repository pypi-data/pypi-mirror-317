from .base_classes import *
from .oscillators import *
import math

class DSBSCModulator(Modulator):
    """
    DSB-SC modulator, in order to modulate DSB-SC you multiply the signal by the carrier, so c*s, i like to think of moving the center frequency, like you know the negative tones? yeah that becomes the lsb part
    """
    def __init__(self, frequency: float, sample_rate: float):
        self.osc = Sine(frequency, sample_rate)
    def modulate(self, signal: float) -> float:
        return self.osc.process()*signal
class AMModulator(Modulator):
    """
    AM modulator based on the DSB-SC modulator (only diffrence is that you have to add the carrier amplitude to your signal)
    """
    def __init__(self, carrier_wave_amplitude:float, frequency: float, sample_rate: float):
        if carrier_wave_amplitude < 0:
            raise ValueError("Carrier wave amplitude must be non-negative.")
        self.cwa = carrier_wave_amplitude
        self.dsbscmod = DSBSCModulator(frequency, sample_rate)
    def modulate(self, signal: float) -> float:
        return self.dsbscmod.modulate(self.cwa+signal)
class FMModulator(Modulator):
    """
    Simple FM Modulator
    Varies the frequency of the oscilator based on the amplitude, this even has a deviation limiter
    """
    def __init__(self, frequency: float, deviation: float, sample_rate: float, deviation_limiter:int=None):
        self.frequency = frequency # Transmission frequency, like where to tune in
        self.deviation = deviation
        self.osc = Sine(frequency, sample_rate) # This is the osciilator we're gonna use, since FM is just a single sine wave but it's freqeuency is changed very fast
        self.deviation_limit = deviation_limiter
    def modulate(self, signal: float) -> float:
        inst_freq = self.frequency + (self.deviation*signal) # Calculate the instantaneous frequency based on the carrier frequency, frequency deviation, and input signal
        # Potentially limit the frequency
        if self.deviation_limit is not None: # Make sure it's on
            if abs(inst_freq-self.frequency) > self.deviation_limit:
                inst_freq = self.frequency + (self.deviation_limit if inst_freq > self.frequency else -self.deviation_limit)
        self.osc.frequency = inst_freq
        return self.osc.process()
class BPSKModulator(Modulator):
    """
    Simple BPSK modulator
    positive phase is phase when its 1 and negative is when its 0
    
    takes phase in radians
    """
    def __init__(self, frequency: float, sample_rate: float, positive_phase: float=math.pi, negetive_phase: float=0.0):
        self.osc = Sine(frequency, sample_rate)
        self.positive_phase = positive_phase
        self.negative_phase = negetive_phase
    def modulate(self, signal: bool):
        return self.osc.process(self.positive_phase if bool(signal) else self.negative_phase) # process takes a phase offset in radians
class QPSKModulator(Modulator):
    """
    Simple QPSK modulator
    00: phase0
    01: phase1
    10: phase2
    11: phase3
    
    takes phase in radians
    """
    def __init__(self, frequency: float, sample_rate: float, phase0: float=0, phase1:float=(math.pi/2), phase2:float = math.pi, phase3:float=(1.5*math.pi)):
        self.osc = Sine(frequency, sample_rate)
        self.phase0 = phase0
        self.phase1 = phase1
        self.phase2 = phase2
        self.phase3 = phase3
    def modulate(self, signal: bool, signal2: bool):
        signal = bool(signal)
        signal2 = bool(signal2)
        if signal and signal2: phase = self.phase3
        elif signal: phase = self.phase2
        elif signal2: phase = self.phase1
        else: phase = self.phase0
        return self.osc.process(phase) # process takes a phase offset in radians
class FSKModulator(Modulator):
    """
    Simple FSK modulator, works a little bit like the FM modulator
    """
    def __init__(self, frequency0: float, frequency1: float, sample_rate: float):
        if frequency0 == frequency1:
            raise Warning("[FSK] Same frequencies?")
        self.freq0 = frequency0
        self.freq1 = frequency1
        self.osc = Sine(frequency0, sample_rate)
    def modulate(self, signal: bool):
        self.osc.frequency = self.freq1 if signal else self.freq0
        return self.osc.process()
class FourFSKModulator(Modulator):
    """
    Simple 4-FSK modulator, works a little bit like the FM modulator
    
    freq0 = 00
    freq1 = 01
    freq2 = 10
    freq3 = 11
    """
    def __init__(self, frequency0: float, frequency1: float, frequency2: float, frequency3: float, sample_rate: float):
        self.freq0 = frequency0
        self.freq1 = frequency1
        self.freq2 = frequency2
        self.freq3 = frequency3
        self.osc = Sine(frequency0, sample_rate)
    def modulate(self, signal: bool, signal2: bool):
        if signal and signal2: freq = self.freq3
        elif signal: freq = self.freq2
        elif signal2: freq = self.freq1
        else: freq = self.freq0
        self.osc.frequency = freq
        return self.osc.process()
