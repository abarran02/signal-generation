from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

import signal_utils as su
from signal_utils import common


def plot_radar_pulse(filename: Path) -> tuple[NDArray[np.complex_], NDArray[np.float_]]:
    sample_rate, bit_length, num_bits, sequence_taps, amplitude, pri, num_pulses = su.radar_pulse.read_input_params(filename)
    seq = common.sequences.maximal_length_sequence(num_bits, np.array(sequence_taps))
    iq_data = su.radar_pulse.generate_pulse(seq, sample_rate, bit_length, pri, num_pulses)
    iq_data = np.round(amplitude * iq_data)

    # fetch number of data points to plot
    t = np.linspace(0, bit_length, iq_data.shape[0])
    return iq_data, t

def plot_cw(filename: Path) -> tuple[NDArray[np.complex_], NDArray[np.float_]]:
    frequency, pw, pri, num_reps, sample_rate = su.continuous_wave.read_input_params(filename)
    iq_data = su.continuous_wave.generate_cw_iq(frequency, pw, pri, num_reps, sample_rate)

    t = np.linspace(0, pw, iq_data.shape[0])
    return iq_data, t

def plot_lfm(filename: Path) -> tuple[NDArray[np.complex_], NDArray[np.float_]]:
    pw, pri, num_reps, fstart, fstop, sample_rate = su.linear_frequency_modulated.read_input_params(filename)
    iq_data = su.linear_frequency_modulated.generate_lfm(pw, pri, num_reps, fstart, fstop, sample_rate)

    t = np.linspace(0, pw, iq_data.shape[0])
    return iq_data, t

if __name__ == "__main__":
    current_file_path = Path(__file__).resolve()
    parent_dir = current_file_path.parent

    # each radar wave type and the example parameter YAML
    waveforms = [
        (plot_radar_pulse, "radar_pulse_example.yaml"),
        (plot_cw, "continuous_wave_example.yaml"),
        (plot_lfm, "lfm_example.yaml")
    ]

    save = False
    # iterate over functions and parameters
    for wave in waveforms:
        # read YAML input file
        filename = parent_dir / "signal_utils" / wave[1]
        # generate data sequence
        iq_data, t = wave[0](filename)

        if save:
            save_filename = f"{wave[1]}.sc16"
            common.binary_file_ops.write_binary_iq_data(save_filename, iq_data)

        # plot radar signal in time domain
        plt.figure()
        plt.plot(t, np.real(iq_data), label="In-phase (I)")
        plt.plot(t, np.imag(iq_data), label="Quadrature (Q)", linestyle="--")
        plt.title("Radar Signal in Time Domain")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.show()
