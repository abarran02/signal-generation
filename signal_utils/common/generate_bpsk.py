# BPSK generation - returns a complex IQ file in the range [-1 + 0j, 1 + 0j]

import math

import numpy as np
from numpy.typing import NDArray

def generate_bpsk(data: NDArray[np.int_], sample_rate: int, bit_length: float) -> NDArray[np.complex_]:
    num_bits = data.shape[0]
    samples_per_bit = math.floor(sample_rate * bit_length)

    iq = np.empty(0)
    for idx in range(num_bits):
        iq = np.append(iq, data[idx] * np.ones([int(samples_per_bit)]))

    # add the complex component
    iq = iq + 1j * np.zeros(iq.shape[0])

    return iq
