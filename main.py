from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import signal_utils as su
from signal_utils import common

def plot_radar_pulse(save=False):
    # read yaml input file
    current_file_path = Path(__file__).resolve()
    parent_dir = current_file_path.parent
    filename = parent_dir / "signal_utils" / "radar_pulse_example.yaml"

    sample_rate, bit_length, num_bits, sequence_taps, amplitude, pri, num_pulses = su.radar_pulse.read_input_params(filename)

    # generate data sequence
    print("Generating IQ file...")
    seq = common.sequences.maximal_length_sequence(num_bits, np.array(sequence_taps))
    pulse_seq = su.radar_pulse.generate_pulse(seq, sample_rate, bit_length, pri, num_pulses)
    pulse_seq = np.round(amplitude * pulse_seq)

    if save:
        # write the IQ data to a binary file
        print("Saving IQ file...")
        save_filename = "radar_pulse_example.sc16"
        common.binary_file_ops.write_binary_iq_data(save_filename, pulse_seq)
        print("Complete!")

    # fetch number of data points to plot
    t = np.linspace(0, bit_length, pulse_seq.shape[0])

    return pulse_seq, t

def plot_cw(save=False):
    current_file_path = Path(__file__).resolve()
    parent_dir = current_file_path.parent
    filename = parent_dir / "signal_utils" / "continuous_wave_example.yaml"

    frequency, pw, pri, num_reps, sample_rate = su.continuous_wave.read_input_params(filename)

    iq_data = su.continuous_wave.generate_cw_iq(frequency, pw, pri, num_reps, sample_rate)

    if save:
        # write IQ data to a binary file
        print("Saving IQ file...")
        save_filename = "cw_example.sc16"
        common.binary_file_ops.write_binary_iq_data(save_filename, iq_data)
        print("Complete!")

    t = np.linspace(0, pw, iq_data.shape[0])
    return iq_data, t

functions = [plot_radar_pulse, plot_cw]

for wave in functions:
    pulse_seq, t = wave()

    # plot radar signal in time domain
    plt.figure()
    plt.plot(t, np.real(pulse_seq), label="In-phase (I)")
    plt.plot(t, np.imag(pulse_seq), label="Quadrature (Q)", linestyle="--")
    plt.title("Radar Signal in Time Domain")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.show()
