from .oscillators import Sine
import math

class AFTELSEncoder:
    """
    Does 4-FSK with a reset tone esentially, follows the AFTE docs in documentation.txt
    """
    def __init__(self, sample_rate: float, time_multiplier: int=1):
        self.tone_200 = Sine(200, sample_rate)
        self.tone_200_sequence = [self.tone_200.process() for _ in range(round(((1/200)/2)*sample_rate))]*time_multiplier # We can't run a tone for a sample, that's becuase you have to run a 1 Hz tone for half a second for atleast one zero crossing
        self.tone_1200 = Sine(1200, sample_rate)
        self.tone_1200_sequence = [self.tone_1200.process() for _ in range(round(((1/1200)/2)*sample_rate))]*time_multiplier
        self.tone_1600 = Sine(1600, sample_rate)
        self.tone_1600_sequence = [self.tone_1600.process() for _ in range(round(((1/1600)/2)*sample_rate))]*time_multiplier
        self.tone_2000 = Sine(2000, sample_rate)
        self.tone_2000_sequence = [self.tone_2000.process() for _ in range(round(((1/2000)/2)*sample_rate))]*time_multiplier
        self.tone_500 = Sine(500, sample_rate)
        self.tone_500_sequence = [self.tone_500.process() for _ in range(round(((1/500)/2)*sample_rate))]*time_multiplier # If a 1 Hz signal requires half a second, then 500 doesnt require 250 seconds, 1 over 500 more like since 1 over 1 is 1, so 1 over 500 and by half is the minimal time to correctly get a signal
    def encode(self, hour: int, minute: int, second: int):
        if hour > 0b111111: raise ValueError("Too large value (h)")
        if minute > 0b111111: raise ValueError("Too large value (m)")
        if second > 0b111111: raise ValueError("Too large value (s)")
        h_bin = bin(hour).removeprefix("0b").zfill(6)
        m_bin = bin(minute).removeprefix("0b").zfill(6)
        s_bin = bin(second).removeprefix("0b").zfill(6)
        if len(h_bin+m_bin+s_bin) != 6*3: raise ValueError("Huh?")
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
class AFTEHSEncoder:
    def __init__(self, sample_rate: float, time_multiplier: int=1):
            self.pilot = Sine(3000, sample_rate) # can't use multisine here
            self.signal = Sine(6000, sample_rate) # can't use multisine here

            self.ff_sequence = [self.signal.process() for _ in range(round(((1/6000)/2)*sample_rate))]*time_multiplier # If a 1 Hz signal requires half a second, then 500 doesnt require 250 seconds, 1 over 500 more like since 1 over 1 is 1, so 1 over 500 and by half is the minimal time to correctly get a signal
            self.signal._phase = 0.0

            self.ft_sequence = [self.signal.process(math.pi/2) for _ in range(round(((1/6000)/2)*sample_rate))]*time_multiplier # If a 1 Hz signal requires half a second, then 500 doesnt require 250 seconds, 1 over 500 more like since 1 over 1 is 1, so 1 over 500 and by half is the minimal time to correctly get a signal
            self.signal._phase = 0.0

            self.tt_sequence = [self.signal.process(math.pi*1.5) for _ in range(round(((1/6000)/2)*sample_rate))]*time_multiplier # If a 1 Hz signal requires half a second, then 500 doesnt require 250 seconds, 1 over 500 more like since 1 over 1 is 1, so 1 over 500 and by half is the minimal time to correctly get a signal
            self.signal._phase = 0.0

            self.tf_sequence = [self.signal.process(math.pi) for _ in range(round(((1/6000)/2)*sample_rate))]*time_multiplier # If a 1 Hz signal requires half a second, then 500 doesnt require 250 seconds, 1 over 500 more like since 1 over 1 is 1, so 1 over 500 and by half is the minimal time to correctly get a signal
            self.signal._phase = 0.0

    def encode(self, year: int, month: int, day: int, utc_offset: int):
        if year > 0b11111: raise ValueError("Too large value (y)")
        if month > 0b1111: raise ValueError("Too large value (m)")
        if day > 0b11111: raise ValueError("Too large value (d)")
        if utc_offset > 0b1111: raise ValueError("Too large value (u)")
        y_bin = bin(year).removeprefix("0b").zfill(6)
        m_bin = bin(month).removeprefix("0b").zfill(4)
        d_bin = bin(day).removeprefix("0b").zfill(6)
        u_bin = bin(utc_offset).removeprefix("0b").zfill(4)
        def modulate(bit_seq: list):
            fun_out = []
            for i in range(len(bit_seq)-1):
                v0, v1 = bool(bit_seq[i]), bool(bit_seq[i+1])
                if v0 and v1:
                    fun_out = self.tt_sequence
                elif v0:
                    fun_out = self.tf_sequence
                elif v1:
                    fun_out = self.ft_sequence
                else:
                    fun_out = self.ff_sequence
            return fun_out
        out = []
        ms_y = modulate(y_bin)
        ms_m = modulate(m_bin)
        ms_d = modulate(d_bin)
        ms_u = modulate(u_bin)
        p_y = [self.pilot.process() for _ in range(len(y_bin))]
        p_m = [self.pilot.process() for _ in range(len(m_bin))]
        p_d = [self.pilot.process() for _ in range(len(d_bin))]
        p_u = [self.pilot.process() for _ in range(len(u_bin))]
        s_y = [(i+j)/2 for (i,j) in zip(ms_y, p_y)]
        s_m = [(i+j)/2 for (i,j) in zip(ms_m, p_m)]
        s_d = [(i+j)/2 for (i,j) in zip(ms_d, p_d)]
        s_u = [(i+j)/2 for (i,j) in zip(ms_u, p_u)]
        out += s_y
        out += s_m
        out += s_d
        out += s_u

class AFTESTSEncoder:
    def __init__(self, sample_rate: float):
        self.gen = Sine(6500, sample_rate)
        self.silence = [0.0]*round(sample_rate*0.9)
        self.pip = [self.gen.process() for _ in range(round(sample_rate*0.1))]
    def encode(self):
            return self.pip + self.silence
class AFTESSTSEncoder:
    def __init__(self, sample_rate: float):
        self.gen = Sine(6500, sample_rate)
        self.silence = [0.0]*round(sample_rate*0.4)
        self.pip = [self.gen.process() for _ in range(round(sample_rate*0.1))]
    def encode(self):
            return self.pip + self.silence + self.pip + self.silence