import math
from pathlib import Path

import numpy as np
import yaml
from numpy.typing import NDArray


def read_input_params(filename: Path) -> tuple[int, float, float, float]:
    """Read radar pulse parameters from input YAML file

    Args:
        filename (Path): YAML file path

    Returns:
        tuple: sample_rate, fstart, fstop, signal_length
    """
    with open(filename, 'r') as file:
        input_params = yaml.safe_load(file)

    return input_params['sample_rate'], input_params['fstart'], input_params['fstop'], input_params['signal_length']

def generate_lfm(sample_rate: int, f_start: float, f_stop: float, signal_length: float, num_pulses: int) -> NDArray[np.complex_]:
    # calculate the number of samples in the RF signal
    num_samples = math.floor(sample_rate * signal_length) 

    # time step
    t = (1.0 / sample_rate) * np.arange(0, num_samples) 

    #v = 1i * 2.0 * M_PI * (f_start * idx * t + (f_stop - f_start) * 0.5 * idx * idx * t * t / signal_length)

    iq = np.exp(1j * 2.0 * np.pi * (f_start * t + (f_stop - f_start) * 0.5 * t * t / signal_length))
    return iq 
   # with_blanks = iq.concatenate(0.0*len(iq))

    #return dup_wave(with_blanks, num_pulses)

def dup_wave(iq: NDArray[np.complex_], num_pulses: int):
   return np.tile(iq, [num_pulses])