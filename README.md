# API Reference

Backend interface to generate radar waveforms with variable parameters and output formats.

## Endpoints

Any numeric value may be expressed as an integer, float, or in scientific notation (e.g. `2.2e3` or `4.5e-6`) and it will be converted accordingly.
Note that the server will not return a warning or error when truncating a float to an int.

The following parameters are used for all API endpoints:

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| sample_rate | int | Yes | Waveform sample rate in hertz |
| form   | string | Yes | Output format either `sc16`, `png`, `graph`, or `threeDim` |
| axes | string | No | For `png` output only, specify `IQvT` or `IvQ` |

All of the following endpoint-specific parameters are required.
Requests missing any parameter will return an HTTP `400 Bad Request`. Available endpoints include:

### [GET] /generate/cw
Generates a Continuous Wave of constant amplitude and frequency.

#### Parameters
| Name | Type | Description |
| --- | --- | --- |
| signal_length | float | Length of output signal in seconds |

### [GET] /generate/radar
Generates a Radar Pulse.

#### Parameters
| Name | Type | Description |
| --- | --- | --- |
| bit_length | float | Symbol duration in seconds |
| num_bits | int | Number of bits to use when randomly generating a maximal length tap sequence |
| amplitude | int | Maximum waveform magnitude |
| pri | float | Time interval between two adjacent pulses in seconds |
| num_pulses | int | Number of radar pulses to generate |

### [GET] /generate/lfm
Generates a Linear Frequency Modulated pulse.

#### Parameters
| Name | Type | Description |
| --- | --- | --- |
| fstart | float | Starting frequency in hertz |
| fstop | float | Ending frequency in hertz |
| signal_length | float | Length of output signal in seconds |

### [GET] /generate/bpsk
Generates a Binary Phase-Shift Keying pulse.

#### Parameters
| Name | Type | Description |
| --- | --- | --- |
| bit_length | float | Symbol duration in seconds |
| num_bits | int | Number of bits to use when randomly generating a maximal length tap sequence |
