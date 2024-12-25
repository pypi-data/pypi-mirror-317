import math

class DiscreteFourierTransform:
    """
    Compute the frequencies that a signal has, it's slow and not exact
    """
    def __init__(self, sample_rate: float):
        self.sr = sample_rate
    def process(self, signal: list) -> list:
        """
        Compute the frequencies that make up a signal using DFT and return strongest frequency in Hz.

        Parameters:
        - signal: List of signal amplitudes (time domain).

        Returns:
        - strongest_frequency: The frequency in Hz with the highest magnitude.
        - magnitudes: Magnitudes of the frequencies in the signal.
        """
        N = len(signal)
        frequencies = [(self.sr * k) / N for k in range(N)]
        magnitudes = []
        
        for k in range(N):  # For each frequency bin
            real_part = 0
            imag_part = 0
            for n in range(N):  # Sum over all time domain samples
                angle = 2 * math.pi * k * n / N
                real_part += signal[n] * math.cos(angle)
                imag_part -= signal[n] * math.sin(angle)
            # Magnitude of the k-th frequency component
            magnitude = math.sqrt(real_part**2 + imag_part**2) / N
            magnitudes.append(magnitude)
        
        half_N = N // 2
        magnitudes = magnitudes[:half_N]
        frequencies = frequencies[:half_N]
        
        max_index = magnitudes.index(max(magnitudes))
        strongest_frequency = frequencies[max_index]
        
        return strongest_frequency, frequencies, magnitudes
class FastFourierTransform:
    """
    The famous Fast Fourier Transform! its fast and exact!
    """
    def __init__(self, sample_rate: float):
        self.sr = sample_rate
    def fft(self, signal):
        N = len(signal)
        if N & (N - 1) != 0:
            raise ValueError("Signal length must be a power of 2.")

        signal = list(signal)  # Ensure mutable
        indices = self._bit_reversal_indices(N)
        signal = [signal[i] for i in indices]

        for step in range(1, int(math.log2(N)) + 1):
            M = 2 ** step
            half_M = M // 2
            twiddle_factors = [
                math.e**(-2j * math.pi * k / M) for k in range(half_M)
            ]
            for start in range(0, N, M):
                for k in range(half_M):
                    even = signal[start + k]
                    odd = twiddle_factors[k] * signal[start + k + half_M]
                    signal[start + k] = even + odd
                    signal[start + k + half_M] = even - odd

        return signal

    def _bit_reversal_indices(self, N):
        bits = int(math.log2(N))
        return [int(bin(i)[2:].zfill(bits)[::-1], 2) for i in range(N)]

    def process(self, signal):
        N = len(signal)
        if N & (N - 1) != 0:
            raise ValueError("Signal length must be a power of 2.")

        frequencies = [(self.sr * k) / N for k in range(N // 2)]
        transformed = self.fft(signal)
        magnitudes = [abs(transformed[k]) / N for k in range(N // 2)]

        max_index = magnitudes.index(max(magnitudes))
        strongest_frequency = frequencies[max_index]

        return strongest_frequency, frequencies, magnitudes