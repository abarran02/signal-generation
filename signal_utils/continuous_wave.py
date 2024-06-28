import math
from pathlib import Path

import numpy as np
import yaml
from numpy.typing import NDArray


def read_input_params(filename: Path) -> tuple[int, float]:
    """Read continuous wave parameters from input YAML file

    Args:
        filename (Path): YAML file path

    Returns:
        tuple: sample_rate, signal_length
    """
    with open(filename, 'r') as file:
        input_params = yaml.safe_load(file)

    return input_params['sample_rate'], input_params['signal_length']

def generate_cw(sample_rate: int, signal_length: float, num_pulses: int) -> NDArray[np.complex_]:

    num_samples = math.floor(sample_rate * signal_length)

    iq = np.ones([int(num_samples)])

    # add the complex component
    iq = iq + 1j * np.zeros(iq.shape[0])

    return dup_wave(iq, num_pulses)

    return iq

def dup_wave(iq: NDArray[np.complex_], num_pulses: int):
   return np.tile(iq, [num_pulses])