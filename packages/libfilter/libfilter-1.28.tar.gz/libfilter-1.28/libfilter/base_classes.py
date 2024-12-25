class StereoFilter:
    # 2 channels -> 2 channels
    def process(self, left: float, right: float) -> tuple:
        return left, right

class MonoFilter:
    # 1 channel -> 1 channel
    def process(self, audio: float) -> float:
        return audio

class SemiStereoFilter:
    # 2 channels -> 1 channel
    def process(self, left: float, right: float) -> float:
        return left

class SemiMonoFilter:
    # 1 channel -> 2 channels
    def process(self, audio: float) -> tuple:
        return audio, audio

class StereoOutput:
    # 0 channels -> 2 channels
    def process(self) -> tuple:
        return 0.0, 0.0

class MonoOutput:
    # 0 channels -> 1 channels
    def process(self) -> float:
        return 0.0

class Oscillator(MonoOutput):
    frequency = -1
    sample_rate = -1

class Modulator:
    def modulate(self, signal):
        return signal

class Demodulator:
    def demodulate(self, signal):
        return signal

class Encoder:
    def encode(self, signal):
        return -int(signal)

class Decoder:
    def decode(self, signal):
        return -int(signal)
