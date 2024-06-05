from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import signal_utils as su

# read yaml input file
current_file_path = Path(__file__).resolve()
parent_dir = current_file_path.parent
filename = parent_dir / "signal_utils" / "radar_pulse_example.yaml"

sample_rate, bit_length, num_bits, sequence_taps, amplitude, pri, num_pulses = su.radar_pulse.read_input_params(filename)

# generate data sequence
seq = su.sequences.maximal_length_sequence(num_bits, np.array(sequence_taps))
pulse_seq = su.radar_pulse.generate_pulse(seq, sample_rate, bit_length, pri, num_pulses)
pulse_seq = np.round(amplitude * pulse_seq)

# fetch number of data points to plot
t = np.linspace(0, bit_length, pulse_seq.shape[0])

# plot radar signal in time domain
plt.figure()
plt.plot(t, np.real(pulse_seq), label="In-phase (I)")
plt.plot(t, np.imag(pulse_seq), label="Quadrature (Q)", linestyle="--")
plt.title("Radar Signal in Time Domain")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.show()
