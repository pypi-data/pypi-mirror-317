from .base_classes import *
from collections import deque
import math

class DiscreteFourierTransform(Transformer):
    """
    Compute the frequencies that a signal has, it's slow and not exact
    """
    def __init__(self, sample_rate: float):
        self.sr = sample_rate
    def transform(self, signal: list) -> list:
        """
        Compute the frequencies that make up a signal using DFT and return strongest frequency in Hz.

        Parameters:
        - signal: list of signal amplitudes (time domain).

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
class FastFourierTransform(Transformer):
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

    def transform(self, signal):
        N = len(signal)
        if N & (N - 1) != 0:
            raise ValueError("Signal length must be a power of 2.")

        frequencies = [(self.sr * k) / N for k in range(N // 2)]
        transformed = self.fft(signal)
        magnitudes = [abs(transformed[k]) / N for k in range(N // 2)]

        max_index = magnitudes.index(max(magnitudes))
        strongest_frequency = frequencies[max_index]

        return strongest_frequency, frequencies, magnitudes
class HilbertTransformer:
    """
    A pure Python implementation of a streaming Hilbert transformer using FIR filter.
    Processes one sample at a time, maintaining an internal buffer.
    """
    def __init__(self, filter_length=101):
        """
        Initialize the streaming Hilbert transformer.
        
        Args:
            filter_length (int): Length of the FIR filter (must be odd)
        """
        if filter_length % 2 != 1:
            raise ValueError("Filter length must be odd")
        
        self.filter_length = filter_length
        self.coefficients = self._calculate_coefficients()
        
        # Initialize buffer with zeros
        self.buffer = deque([0.0] * filter_length, maxlen=filter_length)
        
        # Calculate delay to align output with input
        self.delay_compensation = (filter_length - 1) // 2
        self.delay_buffer = deque([0.0] * self.delay_compensation, maxlen=self.delay_compensation)
        
    def _calculate_coefficients(self):
        """Calculate the FIR filter coefficients for the Hilbert transform."""
        coeffs = []
        half_length = (self.filter_length - 1) // 2
        
        for n in range(-half_length, half_length + 1):
            if n == 0:
                coeffs.append(0.0)
            else:
                # Hilbert transform ideal impulse response
                h = 2 / (math.pi * n)
                # Apply Hamming window for better frequency response
                # w = 0.54 - 0.46 * math.cos(2 * math.pi * (n + half_length) / self.filter_length)
                k = n + half_length
                w = (0.42 - 0.5 * math.cos(2 * math.pi * k / (self.filter_length - 1)) 
                     + 0.08 * math.cos(4 * math.pi * k / (self.filter_length - 1)))
                coeffs.append(h * w)
                
        return coeffs
    
    def transform(self, sample):
        """
        Process a single sample and return its Hilbert transform.
        
        Args:
            sample (float): Input sample value
            
        Returns:
            tuple: (transformed_sample, input_sample)
                  The transformed sample corresponds to the input from
                  delay_compensation samples ago.
        """
        # Add new sample to buffer
        self.buffer.append(sample)
        
        # Calculate filtered sample
        transformed = sum(b * c for b, c in zip(self.buffer, self.coefficients))
        
        # Handle delay compensation
        original = self.delay_buffer[0]
        self.delay_buffer.append(sample)
        
        return transformed, original
    
    def transform_analytic(self, sample):
        """
        Process a single sample and return its analytic signal value.
        
        Args:
            sample (float): Input sample value
            
        Returns:
            complex: The analytic signal value (original + j*hilbert)
        """
        transformed, original = self.transform(sample)
        return complex(original, transformed)
