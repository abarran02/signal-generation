from decimal import Decimal
from pathlib import Path

import numpy as np
import yaml
from numpy.typing import NDArray


def read_input_params(filename: Path) -> tuple[Decimal, Decimal, Decimal, int, int]:
    """Read continuous wave parameters from input YAML file

    Args:
        filename (Path): YAML file path

    Returns:
        tuple: frequency, pulse_width, pri, num_reps, sample_rate
    """
    with open(filename, 'r') as file:
        input_params = yaml.safe_load(file)

    return input_params['frequency'], input_params['pulse_width'], input_params['pri'], input_params['num_reps'], input_params['sample_rate']


def generate_cw_iq(frequency: Decimal, pw: Decimal, pri: Decimal, num_reps: int, sample_rate: int) -> NDArray[np.complex_]:
    """Generate a pulsed wave signal

    Args:
        frequency (Decimal): The frequency of the continuous wave in Hz
        pw (Decimal): Pulse width in seconds
        pri (Decimal): Pulse repetition interval in seconds
        num_reps (int): Number of repetitions of the pulse
        sample_rate (Decimal): The sample rate in samples per second (Hz)

    Returns:
        np.ndarray: A numpy array of complex values representing the pulsed wave
    """
    # Number of samples per pulse
    num_samples_pw = int(pw * sample_rate)
    # Number of samples per pulse repetition interval
    num_samples_pri = int(pri * sample_rate)

    # Generate one pulse
    t_pulse = np.arange(0, pw, 1/sample_rate)
    i_pulse = np.cos(2 * np.pi * frequency * t_pulse)
    q_pulse = np.sin(2 * np.pi * frequency * t_pulse)
    iq_pulse = i_pulse + 1j * q_pulse

    # Create a zero array for the full PRI period
    iq_pri = np.zeros(num_samples_pri, dtype=complex)
    # Insert the pulse into the PRI period
    iq_pri[:num_samples_pw] = iq_pulse

    # Repeat the pulse over the number of repetitions
    iq_waveform = np.tile(iq_pri, num_reps)

    return iq_waveform
