from .base_classes import *
import math

#region Clippers
class MonoClipper(MonoFilter):
    """
    Limits incoming audio to -1.0 or 1.0
    """
    def process(self, audio: float):
        return (max(min(audio,1.0),-1.0))
class StereoClipper(StereoFilter):
    """
    Does the same thing as the mono version but stereo
    """
    def process(self, left: float, right: float):
        return (max(min(left,1.0),-1.0)), (max(min(right,1.0),-1.0)) 
class MonoDeclipper:
    """
    This does linear interpolation
    
    If a sample is clipped, it tries to guess what that sample could be, so like if we have 0.5 and then 1, 0.75 could be in the middle
    """
    def __init__(self, threshold: float=1.0) -> None:
        self.threshold = threshold
    def process(self, prev_audio: float, current_audio: float, future_audio: float):
        if current_audio > self.threshold or current_audio < -self.threshold:
            # If the audio is clipped, restore it by linear interpolation
            return (prev_audio + future_audio) / 2
        else:
            # Limit the audio to the range [-1.0, 1.0]
            return max(min(current_audio, 1.0), -1.0)
class StereoDeclipper:
    """
    Stereo version of the mono one
    """
    def __init__(self, threshold: float=1.0) -> None:
        self.declipper_l = MonoDeclipper(threshold)
        self.declipper_r = MonoDeclipper(threshold)
    def process(self, prev_audio_l: float, prev_audio_r: float, current_audio_l: float, current_audio_r: float, future_audio_l: float, future_audio_r: float) -> tuple:
        return self.declipper_l.process(prev_audio_l, current_audio_l, future_audio_l), self.declipper_r.process(prev_audio_r, current_audio_r, future_audio_r)
#endregion Clippers

class StereoToMono(SemiStereoFilter):
    """
    Converts 2 channels into one using averaging ([a+b]/2)
    """
    def process(self, left: float, right: float):
        return ((left + right) / 2)

class MonoFadeOut(MonoFilter):
    """
    Makes a linear fade out
    
    Logarithmically decreases the amplitude of the signal by 1/(sample_rate*duration), if you supply DC to it then you'd see it go from 1 to 0
    """
    def __init__(self, duration: float, sample_rate: float, allow_negative_amplitude:bool=False):
        self.duration = duration
        self.sr = sample_rate
        self.decrement = None
        self.amplitude = 1.0
        self.reset()
        self.allow_negative_amplitude = allow_negative_amplitude
    def reset(self):
        self.decrement = 1/(self.sr*self.duration)
        self.amplitude = 1.0
    def process(self, audio: float) -> float:
        if not self.allow_negative_amplitude:
            self.amplitude = max(0.0, self.amplitude)
        sample = audio * self.amplitude
        self.amplitude -= self.decrement
        return sample
class StereoFadeOut(StereoFilter):
    def __init__(self, duration: float, sample_rate: float, allow_negative_amplitude:bool=True):
        self.fo_l = MonoFadeOut(duration, sample_rate, allow_negative_amplitude)
        self.fo_r = MonoFadeOut(duration, sample_rate, allow_negative_amplitude)
    def reset(self):
        self.fo_l.reset()
        self.fo_r.reset()
    def process(self, left:float, right: float) -> tuple[float,float]:
        return self.fo_l.process(left), self.fo_r.process(right)
class MonoFadeIn(MonoFilter):
    """
    Makes a linear fade in
    """
    def __init__(self, duration: float, sample_rate: float):
        self.duration = duration
        self.sr = sample_rate
        self.decrement = None
        self.amplitude = 0.0
        self.reset()
    def reset(self):
        self.decrement = 1/(self.sr*self.duration)
        self.amplitude = 0.0
    def process(self, audio: float) -> float:
        self.amplitude = min(1.0, self.amplitude)
        sample = audio * self.amplitude
        self.amplitude += self.decrement
        return sample
class StereoFadeIn(StereoFilter):
    def __init__(self, duration: float, sample_rate: float, dont_inverse:bool=True):
        self.fi_l = MonoFadeIn(duration, sample_rate, dont_inverse)
        self.fi_r = MonoFadeIn(duration, sample_rate, dont_inverse)
    def reset(self):
        self.fi_l.reset()
        self.fi_r.reset()
    def process(self, left:float, right: float) -> tuple[float,float]:
        return self.fi_l.process(left), self.fi_r.process(right)

#region Compressors
class StereoRpitxCompressor(StereoFilter):
    """
    This is the broadcast compressor that can be found in pifmrds
    This is a peak compressor
    """
    def __init__(self, attack: float, decay: float, mgr:float=0.01) -> None:
        self.lmax = 0.0
        self.rmax = 0.0
        self.attack = attack
        self.decay = decay
        self.mgr = mgr
    def process(self, left: float, right: float):
        l_abs = abs(left)
        if l_abs > self.lmax:
            self.lmax += (l_abs - self.lmax)*self.attack
        else:
            self.lmax *= self.decay
        r_abs = abs(right)
        if r_abs > self.rmax:
            self.rmax += (r_abs - self.rmax)*self.attack
        else:
            self.rmax *= self.decay
        if self.lmax > self.rmax: self.rmax = self.lmax
        elif self.rmax > self.lmax: self.lmax = self.rmax
        return left/(self.lmax+self.mgr), right/(self.rmax+self.mgr)
class MonoRpitxCompressor(MonoFilter):
    """
    This is the broadcast compressor that can be found in pifmrds but mono
    """
    def __init__(self, attack: float, decay: float, mgr:float=0.01) -> None:
        self.max = 0.0
        self.attack = attack
        self.decay = decay
        self.mgr = mgr
    def process(self, audio: float):
        a_abs = abs(audio)
        if a_abs > self.max:
            self.max += (a_abs - self.max)*self.attack
        else:
            self.max *= self.decay
        return audio/(self.max+self.mgr)
#endregion Compressors

#region Frequency Filters
class MonoExponentialLPF(MonoFilter):
    """
    A simple low-pass filter using exponential smoothing.
    
    Args:
        cutoff_frequency (float): The cutoff frequency in Hz.
        sampling_rate (float): The sampling rate in Hz.
    """
    def __init__(self, cutoff_frequency: float, sampling_rate: float):
        if cutoff_frequency <= 0 or sampling_rate <= 0:
            raise ValueError("cutoff_frequency and sampling_rate must be positive.")
        if cutoff_frequency >= sampling_rate / 2:
            raise ValueError("cutoff_frequency must be less than half the sampling rate (Nyquist limit).")
        self.cutoff_frequency = cutoff_frequency
        self.sampling_rate = sampling_rate
        # Calculate the smoothing factor (alpha)
        rc = 1 / (2 * math.pi * cutoff_frequency)  # Time constant (RC)
        self.alpha = sampling_rate / (sampling_rate + rc)  # Adjust for discrete sampling
        self.previous_output = None
    def process(self, audio: float):
        """
        Applies the low-pass filter to a single input sample.
        
        Args:
            audio (float): The input audio sample.
        
        Returns:
            float: The filtered output sample.
        """
        if self.previous_output is None:
            self.previous_output = audio  # Initialize with the first sample
        # Calculate the filtered output
        output_sample = self.alpha * audio + (1 - self.alpha) * self.previous_output
        self.previous_output = output_sample
        return output_sample
class StereoExponentialLPF(StereoFilter):
    def __init__(self, cutoff_frequency: float, sampling_rate: float) -> None:
        self.lpf_l = MonoExponentialLPF(cutoff_frequency, sampling_rate)
        self.lpf_r = MonoExponentialLPF(cutoff_frequency, sampling_rate)
    def process(self, left: float, right: float) -> tuple:
        return self.lpf_l.process(left), self.lpf_r.process(right)
class MonoExponentialHPF(MonoFilter):
    def __init__(self, cutoff_frequency: float, sampling_rate: float):
        if cutoff_frequency <= 0 or sampling_rate <= 0:
            raise ValueError("cutoff_frequency and sampling_rate must be positive.")
        if cutoff_frequency >= sampling_rate / 2:
            raise ValueError("cutoff_frequency must be less than half the sampling rate (Nyquist limit).")
            
        self.cutoff_frequency = cutoff_frequency
        self.sampling_rate = sampling_rate
        
        # Calculate the smoothing factor (alpha)
        rc = 1 / (2 * math.pi * cutoff_frequency)
        self.alpha = rc / (rc + 1/sampling_rate)
        
        self.previous_input = None
        self.previous_output = None

    def process(self, audio: float):
        if self.previous_input is None:
            self.previous_input = audio
            self.previous_output = 0
            return 0
        output_sample = self.alpha * (self.previous_output + audio - self.previous_input)
        
        self.previous_input = audio
        self.previous_output = output_sample
        
        return output_sample
class StereoExponentialHPF(StereoFilter):
    def __init__(self, cutoff_frequency: float, sampling_rate: float) -> None:
        self.hpf_l = MonoExponentialHPF(cutoff_frequency, sampling_rate)
        self.hpf_r = MonoExponentialHPF(cutoff_frequency, sampling_rate)
    def process(self, left: float, right: float) -> tuple:
        return self.hpf_l.process(left), self.hpf_r.process(right)
class MonoButterworthLPF(MonoFilter):
    def __init__(self, cutoff_freq: float, sample_rate: float, order: int = 2):
        super().__init__()
        self.cutoff_freq = cutoff_freq
        self.sample_rate = sample_rate
        self.order = order
        
        # Intermediate calculation values
        f = math.tan(math.pi * cutoff_freq / sample_rate)
        self.a = [0.0] * (order + 1)  # denominator coefficients
        self.b = [0.0] * (order + 1)  # numerator coefficients
        
        # Calculate coefficients for 2nd order sections
        if order == 2:
            # Prototype Butterworth polynomials for 2nd order
            q = math.sqrt(2.0)  # Q factor for Butterworth response
            
            # Bilinear transform coefficients
            ff = f * f
            self.b[0] = ff
            self.b[1] = 2.0 * ff
            self.b[2] = ff
            self.a[0] = 1.0 + (2.0 * f / q) + ff
            self.a[1] = 2.0 * (ff - 1.0)
            self.a[2] = 1.0 - (2.0 * f / q) + ff
            
            # Normalize coefficients
            for i in range(3):
                self.b[i] /= self.a[0]
            self.a[1] /= self.a[0]
            self.a[2] /= self.a[0]
            self.a[0] = 1.0
        
        # Initialize state variables for the filter
        self.x = [0.0] * (order + 1)  # input history
        self.y = [0.0] * (order + 1)  # output history
    
    def process(self, audio: float) -> float:
        # Shift the previous values
        for i in range(self.order, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        # Add new input
        self.x[0] = audio
        
        # Calculate new output
        self.y[0] = self.b[0] * self.x[0]
        for i in range(1, self.order + 1):
            self.y[0] += self.b[i] * self.x[i] - self.a[i] * self.y[i]
        
        return self.y[0]
    
    def reset(self):
        self.x = [0.0] * (self.order + 1)
        self.y = [0.0] * (self.order + 1)
class StereoButterworthLPF(StereoFilter):
    def __init__(self, cutoff_frequency: float, sampling_rate: float, order: int=2) -> None:
        self.lpf_l = MonoButterworthLPF(cutoff_frequency, sampling_rate, order)
        self.lpf_r = MonoButterworthLPF(cutoff_frequency, sampling_rate, order)
    def process(self, left: float, right: float) -> tuple:
        return self.lpf_l.process(left), self.lpf_r.process(right)
class MonoButterworthHPF(MonoFilter):
    def __init__(self, cutoff_freq: float, sample_rate: float, order: int = 2):
        super().__init__()
        self.cutoff_freq = cutoff_freq
        self.sample_rate = sample_rate
        self.order = order
        
        # Intermediate calculation values
        f = math.tan(math.pi * cutoff_freq / sample_rate)
        self.a = [0.0] * (order + 1)  # denominator coefficients
        self.b = [0.0] * (order + 1)  # numerator coefficients
        
        # Calculate coefficients for 2nd order sections
        if order == 2:
            # Prototype Butterworth polynomials for 2nd order
            q = math.sqrt(2.0)  # Q factor for Butterworth response
            
            # Bilinear transform coefficients
            ff = f * f
            self.b[0] = 1.0
            self.b[1] = -2.0
            self.b[2] = 1.0
            self.a[0] = 1.0 + (2.0 * f / q) + ff
            self.a[1] = 2.0 * (ff - 1.0)
            self.a[2] = 1.0 - (2.0 * f / q) + ff
            
            # Normalize coefficients
            for i in range(3):
                self.b[i] /= self.a[0]
            self.a[1] /= self.a[0]
            self.a[2] /= self.a[0]
            self.a[0] = 1.0
        
        # Initialize state variables for the filter
        self.x = [0.0] * (order + 1)  # input history
        self.y = [0.0] * (order + 1)  # output history
    
    def process(self, audio: float) -> float:
        # Shift the previous values
        for i in range(self.order, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        # Add new input
        self.x[0] = audio
        
        # Calculate new output
        self.y[0] = self.b[0] * self.x[0]
        for i in range(1, self.order + 1):
            self.y[0] += self.b[i] * self.x[i] - self.a[i] * self.y[i]
        
        return self.y[0]
    
    def reset(self):
        self.x = [0.0] * (self.order + 1)
        self.y = [0.0] * (self.order + 1)
class StereoButterworthHPF(StereoFilter):
    def __init__(self, cutoff_frequency: float, sampling_rate: float, order: int=2) -> None:
        self.hpf_l = MonoButterworthHPF(cutoff_frequency, sampling_rate, order)
        self.hpf_r = MonoButterworthHPF(cutoff_frequency, sampling_rate, order)
    def process(self, left: float, right: float) -> tuple:
        return self.hpf_l.process(left), self.hpf_r.process(right)
class MonoButterworthBPF(MonoFilter):
    def __init__(self, low_freq: float, high_freq: float, sample_rate: float, order: int = 2):
        super().__init__()
        self.low_freq = low_freq
        self.high_freq = high_freq
        self.sample_rate = sample_rate
        self.order = order
        
        # Intermediate calculation values
        w0 = 2.0 * math.pi * math.sqrt(low_freq * high_freq) / sample_rate  # Center frequency
        bw = 2.0 * math.pi * (high_freq - low_freq) / sample_rate  # Bandwidth
        
        # Prewarp frequencies
        w0_warped = math.tan(w0 / 2.0)
        bw_warped = math.tan(bw / 2.0)
        
        # Calculate coefficients
        q = 2.0 * w0_warped / bw_warped  # Q factor
        wc = w0_warped
        
        # Denominator coefficients
        self.a = [0.0] * (order + 1)
        # Numerator coefficients
        self.b = [0.0] * (order + 1)
        
        if order == 2:
            # Butterworth bandpass coefficients
            norm = 1.0 / (1.0 + wc/q + wc*wc)
            
            self.b[0] = wc/q * norm
            self.b[1] = 0.0
            self.b[2] = -wc/q * norm
            
            self.a[0] = 1.0
            self.a[1] = -2.0 * (wc*wc - 1.0) * norm
            self.a[2] = (1.0 - wc/q + wc*wc) * norm
        
        # Initialize state variables
        self.x = [0.0] * (order + 1)  # input history
        self.y = [0.0] * (order + 1)  # output history
    
    def process(self, audio: float) -> float:
        # Shift the previous values
        for i in range(self.order, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        # Add new input
        self.x[0] = audio
        
        # Calculate new output
        self.y[0] = self.b[0] * self.x[0]
        for i in range(1, self.order + 1):
            self.y[0] += self.b[i] * self.x[i] - self.a[i] * self.y[i]
        
        return self.y[0]
    
    def reset(self):
        self.x = [0.0] * (self.order + 1)
        self.y = [0.0] * (self.order + 1)
class StereoButterworthBPF(StereoFilter):
    def __init__(self, low_freq: float, high_freq: float, sample_rate: float, order: int = 2) -> None:
        self.bpf_l = MonoButterworthBPF(low_freq, high_freq, sample_rate, order)
        self.bpf_r = MonoButterworthBPF(low_freq, high_freq, sample_rate, order)
    def process(self, left: float, right: float) -> tuple:
        return self.bpf_l.process(left), self.bpf_r.process(right)
#endregion Frequency Filters

#region Emphasis
class MonoPreemphasis(MonoFilter):
    """
    Pre-emphasis, useful for transmissions
    """
    def __init__(self, microsecond_tau: float, sample_rate: float) -> None:
        tau_seconds = microsecond_tau / 1_000_000
        self.alpha = math.exp(-1 / (tau_seconds * sample_rate))
        self.prevsample = None
    def process(self, audio: float) -> float:
        if self.prevsample is None:
            self.prevsample = audio
            return audio
        sample = audio - self.alpha * self.prevsample
        self.prevsample = sample
        return sample
class StereoPreemphasis(StereoFilter):
    def __init__(self, microsecond_tau: float, sample_rate: float) -> None:
        self.filter_l = MonoPreemphasis(microsecond_tau, sample_rate)
        self.filter_r = MonoPreemphasis(microsecond_tau, sample_rate)
    def process(self, left: float, right: float) -> tuple:
        return self.filter_l.process(left), self.filter_r.process(right)
class MonoDeemphasis(MonoFilter):
    def __init__(self, microsecond_tau: float, sample_rate: float) -> None:
        tau_seconds = microsecond_tau / 1_000_000
        self.alpha = math.exp(-1 / (tau_seconds * sample_rate))
        self.prevsample = None
    def process(self, audio: float) -> float:
        if self.prevsample is None:
            self.prevsample = audio
            return audio
        sample = audio + self.alpha * self.prevsample
        self.prevsample = sample
        return sample
class StereoDeemphasis(StereoFilter):
    def __init__(self, microsecond_tau: float, sample_rate: float) -> None:
        self.filter_l = MonoDeemphasis(microsecond_tau, sample_rate)
        self.filter_r = MonoDeemphasis(microsecond_tau, sample_rate)
    def process(self, left: float, right: float) -> tuple:
        return self.filter_l.process(left), self.filter_r.process(right)
#endregion Emphasis