from pathlib import Path

import numpy as np
import yaml
from numpy.typing import NDArray

from .common.filter_windows import create_fir_filter, nuttall_window, blackman_nuttall_window
from .common.generate_bpsk import generate_bpsk


def read_input_params(filename: Path) -> tuple[int, float, int, list[int], int, float, int]:
    """Read radar pulse parameters from input YAML file

    Args:
        filename (Path): YAML file path

    Returns:
        tuple: sample_rate, bit_length, num_bits, taps, amplitude, pri, num_pulses
    """
    with open(filename, 'r') as file:
        input_params = yaml.safe_load(file)

    return input_params['sample_rate'], input_params['bit_length'], input_params['num_bits'], input_params['taps'], \
        input_params['amplitude'], input_params['pri'], input_params['num_pulses']

def user_generate_pulse(fc, num_taps, seq, sample_rate, bit_length, pri, num_pulses):
    samples_per_pulse = int(sample_rate * pri)
        
    pulse = generate_bpsk(seq, sample_rate, bit_length)

    pulse_buffer = int(samples_per_pulse - pulse.shape[0])
    if (pulse_buffer < 0):
        pulse_buffer = 0

    pulse = np.append(pulse, np.zeros([pulse_buffer]))

    w = blackman_nuttall_window(num_taps)
    lpf = create_fir_filter(fc, w)
    
    pulse_filt = np.convolve(pulse, lpf[::-1], "same")

    # normalize the pulse
    pulse_max = np.max(np.abs(pulse_filt))
    pulse_filt = pulse_filt/pulse_max

    # append multiple copies
    pulse_seq = np.tile(pulse_filt, [num_pulses])

    return pulse_seq


def generate_pulse(seq: NDArray[np.int_], sample_rate: int, bit_length: float, pri: float, num_pulses: int) -> NDArray[np.complex_]:
    samples_per_pulse = int(sample_rate * pri)

    pulse = generate_bpsk(seq, sample_rate, bit_length)

    # add zeros to the end of the pulse until the pri is satisfied
    pulse_buffer = int(samples_per_pulse - pulse.shape[0])
    if (pulse_buffer < 0):
        pulse_buffer = 0

    pulse = np.append(pulse, np.zeros([pulse_buffer]))

    # create the filter parameters
    fc = (2.1/bit_length)/sample_rate
    num_taps = 501

    # create the filter
    w = nuttall_window(num_taps)
    lpf = create_fir_filter(fc, w)

    # filter the pulse
    pulse_filt = np.convolve(pulse, lpf[::-1], "same")

    # normalize the pulse
    pulse_max = np.max(np.abs(pulse_filt))
    pulse_filt = pulse_filt/pulse_max

    # append multiple copies
    pulse_seq = np.tile(pulse_filt, [num_pulses])

    return pulse_seq
