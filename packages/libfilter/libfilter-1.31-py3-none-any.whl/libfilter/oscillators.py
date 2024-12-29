from .base_classes import *
import math

class Sine(Oscillator):
    """
    Generates a sine wave of a selected frequency and sample rate, allowing dynamic frequency changes.
    """
    def __init__(self, frequency: float, sampling_rate: float) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate

    def process(self, phase_offset: float = 0.0) -> float:
        # Compute the sample
        sample = math.sin(self._phase + phase_offset)
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        return sample
class MultiSine(Oscillator):
    """
    Generates a sine wave of a selected frequency and sample rate, allowing dynamic frequency changes. Also returns harmonics
    """
    def __init__(self, frequency: float, sampling_rate: float, harmonics: int) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        self.harmonics = harmonics

    def process(self, phase_offset: float = 0.0) -> float:
        out = []
        # Compute the sample(s)
        for i in range(self.harmonics+1):
            out.append(math.sin((self._phase*(i+1)) + phase_offset))
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        return out
class SquareOoscillator(Oscillator):
    """
    Generates a square wave of a selected frequency and sample rate, allowing dynamic frequency changes.
    """
    def __init__(self, frequency: float, sampling_rate: float) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate

    def process(self, phase_offset: float = 0.0) -> float:
        # Compute the sample
        sample = math.sin(self._phase + phase_offset)
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        # Convert sine wave into square wave
        sample = 1.0 if sample >= 0 else -1.0
        return sample
class MultiSquareoscillator(Oscillator):
    """
    Generates a square wave of a selected frequency and sample rate, allowing dynamic frequency changes. Also returns harmonics
    """
    def __init__(self, frequency: float, sampling_rate: float, harmonics: int) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        self.harmonics = harmonics

    def process(self, phase_offset: float = 0.0) -> float:
        out = []
        # Compute the sample(s)
        for i in range(self.harmonics+1):
            out.append(math.sin((self._phase*(i+1)) + phase_offset))
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        # Convert sine wave into square wave
        out = [1.0 if i >= 0 else -1.0 for i in out]
        return out
class Triangle(Oscillator):
    """
    Generates a triangle wave of a selected frequency and sample rate, allowing dynamic frequency changes.
    """
    def __init__(self, frequency: float, sampling_rate: float) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate

    def process(self, phase_offset: float = 0.0) -> float:
        # Compute the sample
        sample = math.sin(self._phase + phase_offset)
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        # Convert sine wave into triangle wave
        sample = (2 / math.pi) * math.asin(sample)
        return sample
class MultiTriangle(Oscillator):
    """
    Generates a triangle wave of a selected frequency and sample rate, allowing dynamic frequency changes. Also returns harmonics
    """
    def __init__(self, frequency: float, sampling_rate: float, harmonics: int) -> None:
        self.sample_rate = sampling_rate
        self.frequency = frequency
        self._phase = 0.0
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        self.harmonics = harmonics

    def process(self, phase_offset: float = 0.0) -> float:
        out = []
        # Compute the sample(s)
        for i in range(self.harmonics+1):
            out.append(math.sin((self._phase*(i+1)) + phase_offset))
        # Update phase increment
        self._phase_increment = (2 * math.pi * self.frequency) / self.sample_rate
        # Increment phase and wrap around to prevent overflow
        self._phase = (self._phase + self._phase_increment) % (2 * math.pi)
        # Convert sine wave into triangle wave
        out = [(2 / math.pi) * math.asin(i) for i in out]
        return out
