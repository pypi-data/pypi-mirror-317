class StereoFilter:
    # 2 channels -> 2 channels
    def process(self, left: float, right: float) -> tuple:
        raise NotImplementedError

class MonoFilter:
    # 1 channel -> 1 channel
    def process(self, audio: float) -> float:
        raise NotImplementedError

class SemiStereoFilter:
    # 2 channels -> 1 channel
    def process(self, left: float, right: float) -> float:
        raise NotImplementedError

class SemiMonoFilter:
    # 1 channel -> 2 channels
    def process(self, audio: float) -> tuple:
        raise NotImplementedError

class StereoOutput:
    # 0 channels -> 2 channels
    def process(self) -> tuple:
        raise NotImplementedError

class MonoOutput:
    # 0 channels -> 1 channels
    def process(self) -> float:
        raise NotImplementedError

class Oscillator(MonoOutput):
    frequency = -1
    sample_rate = -1

class Modulator:
    def modulate(self, signal):
        raise NotImplementedError

class Demodulator:
    def demodulate(self, signal):
        raise NotImplementedError

class Encoder:
    def encode(self, signal):
        raise NotImplementedError

class Decoder:
    def decode(self, signal):
        raise NotImplementedError

class Transformer:
    def transform(self, signal):
        raise NotImplementedError
