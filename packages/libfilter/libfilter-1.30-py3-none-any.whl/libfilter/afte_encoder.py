from .oscillators import Sine

class AFTELSEncoder:
    """
    Does 4-FSK with a reset tone esentially, follows the AFTE docs in documentation.txt
    """
    def __init__(self, sample_rate: float):
        self.tone_200 = Sine(200, sample_rate)
        self.tone_200_sequence = [self.tone_200.process() for _ in range(round(((1/200)/2)*sample_rate))] # We can't run a tone for a sample, that's becuase you have to run a 1 Hz tone for half a second for atleast one zero crossing
        self.tone_1200 = Sine(1200, sample_rate)
        self.tone_1200_sequence = [self.tone_1200.process() for _ in range(round(((1/1200)/2)*sample_rate))]
        self.tone_1600 = Sine(1600, sample_rate)
        self.tone_1600_sequence = [self.tone_1600.process() for _ in range(round(((1/1600)/2)*sample_rate))]
        self.tone_2000 = Sine(2000, sample_rate)
        self.tone_2000_sequence = [self.tone_2000.process() for _ in range(round(((1/2000)/2)*sample_rate))]
        self.tone_500 = Sine(500, sample_rate)
        self.tone_500_sequence = [self.tone_500.process() for _ in range(round(((1/500)/2)*sample_rate))]
    def encode(self, hour: int, minute: int, second: int):
        if hour > 0b111111: raise ValueError("Too large value (h)")
        if minute > 0b111111: raise ValueError("Too large value (m)")
        if second > 0b111111: raise ValueError("Too large value (s)")
        h_bin = bin(hour).removeprefix("0b").zfill(6)
        m_bin = bin(minute).removeprefix("0b").zfill(6)
        s_bin = bin(second).removeprefix("0b").zfill(6)
        out = []
        def modulate(bit_seq: list):
            fun_out = []
            for i in range(len(bit_seq)-1):
                v0, v1 = bool(bit_seq[i]), bool(bit_seq[i+1])
                if v0 and v1:
                    fun_out += self.tone_1600_sequence
                elif v0:
                    fun_out += self.tone_2000_sequence 
                elif v1:
                    fun_out += self.tone_1200_sequence
                else:
                    fun_out += self.tone_200_sequence
            return fun_out
        out += modulate(h_bin)
        out += modulate(m_bin)
        out += modulate(s_bin)
        out += self.tone_500_sequence
        return out
class AFTESTSEncoder:
    def __init__(self, sample_rate: float):
        self.gen = Sine(6500, sample_rate)
        self.silence = [0.0]*round(sample_rate*0.9)
        self.pip = [self.gen.process() for _ in range(round(sample_rate*0.1))]
    def encode(self):
            return self.pip + self.silence        