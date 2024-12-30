from .base_classes import *

class DiffrentialDecoder(Encoder):
    """
    Diffrential decoder, starts with 0, and every 1 is so it changed, so for example to encode 0b1100 you have it being 0b1010
    """
    def __init__(self, preamble:bool=False):
        self.last_bit = preamble
    def decode(self, signal: bool) -> bool:
        out = self.last_bit^signal # that also works on bools
        self.last_bit = out
        return out