import math
class Buffer:
    """
    Buffer, each sample you write to it gets saved and when there's enough samples the process function returns a list of the samples you saved
    """
    def __init__(self, buffer_size: int):
        self.size = buffer_size
        self.buffer = []
    def process(self, sample):
        self.buffer.append(sample)
        if len(self.buffer) >= self.size:
            b = self.buffer
            self.buffer.clear()
            return b
class RMSCalculator:
    """
    Calculates the RMS of the samples in the list
    """
    def process(self, samples: list):
        if len(samples) == 0: raise Exception("0 samples? More like 0 IQ")
        squared = [sample**2 for sample in samples]
        mean = sum(squared)/len(squared)
        root = math.sqrt(mean)
        return root