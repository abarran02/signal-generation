from decimal import Decimal
from pathlib import Path

import numpy as np
import yaml
from numpy.typing import NDArray


def read_input_params(filename: Path) -> tuple[Decimal, Decimal, int, Decimal, Decimal, int]:
    """Read radar pulse parameters from input YAML file

    Args:
        filename (Path): YAML file path

    Returns:
        tuple: pulse_width, pri, num_reps, fstart, fstop, sample_rate
    """
    with open(filename, 'r') as file:
        input_params = yaml.safe_load(file)

    return input_params['pulse_width'], input_params['pri'], input_params['num_reps'], input_params['fstart'], input_params['fstop'], input_params['sample_rate']

def generate_lfm(pw: Decimal, pri: Decimal, num_reps: int, fstart: Decimal, fstop: Decimal, sample_rate: int) -> NDArray[np.complex_]:
    """Generate a Linear Frequency Modulated (LFM) pulsed wave signal

    Args:
        pw (Decimal): Pulse width in seconds
        pri (Decimal): Pulse repetition interval in seconds
        num_reps (int): Number of repetitions of the pulse
        fstart (Decimal): Start frequency of the LFM pulse in Hz
        fstop (Decimal): Stop frequency of the LFM pulse in Hz
        sample_rate (int): The sample rate in samples per second (Hz)

    Returns:
        np.ndarray: A numpy array of complex values representing the LFM pulsed wave.
    """
    # Number of samples per pulse
    num_samples_pw = int(pw * sample_rate)
    # Number of samples per pulse repetition interval
    num_samples_pri = int(pri * sample_rate)

    # Time vector for one pulse
    t_pulse = np.linspace(0, pw, num_samples_pw, endpoint=False)

    # Generate the LFM pulse
    k = (fstop - fstart) / pw  # Chirp rate
    i_pulse = np.cos(2 * np.pi * (fstart * t_pulse + 0.5 * k * t_pulse**2))
    q_pulse = np.sin(2 * np.pi * (fstart * t_pulse + 0.5 * k * t_pulse**2))
    iq_pulse = i_pulse + 1j * q_pulse

    # Create a zero array for the full PRI period
    iq_pri = np.zeros(num_samples_pri, dtype=complex)
    # Insert the pulse into the PRI period
    iq_pri[:num_samples_pw] = iq_pulse

    # Repeat the pulse over the number of repetitions
    iq_waveform = np.tile(iq_pri, num_reps)

    return iq_waveform
