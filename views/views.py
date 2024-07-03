import numpy as np
from flask import Blueprint, request
from marshmallow import ValidationError

import signal_utils as su
from signal_utils.common.sequences import generate_fbpsk

from .response import output_cases
from .schema import *

wave_views = Blueprint("wave_views", __name__, url_prefix="/generate")

# generates the designated pulse where each pulse repetition interval (pri) = pulse width + zeros for the remaining space
# returns the pulse to be displayed by output_cases
@wave_views.route("/cw", methods=["GET"])
def get_cw():
    schema = CWSchema()

    try:
        data = schema.load(request.args)
        pulse = su.continuous_wave.generate_cw(data["sample_rate"], data["signal_length"])
        pulse = get_pulse_blanks(pulse, 1, data["amplitude"], data["signal_length"], data["sample_rate"], data["pw"], "cw")

        return output_cases(pulse, data["form"], data["signal_length"], "CW", data["axes"], 1, False)

    except ValidationError as err:
        return {"errors": err.messages}, 400

@wave_views.route("/lfm", methods=["GET"])
def get_lfm():
    schema = LFMSchema()
    i = 0
    try:
        data = schema.load(request.args)
        pulse = su.linear_frequency_modulated.generate_lfm(data["sample_rate"], data["fstart"], data['fstop'], data["pri"], data["num_pulses"])
        pulse = get_pulse_blanks(pulse, data["num_pulses"], data["amplitude"], data["pri"], data["sample_rate"],  data["pw"], "lfm")
        pulse = np.tile(pulse, data["num_pulses"])


        return output_cases(pulse, data["form"], data["pri"], "lfm", data["axes"], data["num_pulses"],False)
        

    except ValidationError as err:
        return {"errors": err.messages}, 400

#For each pulse, create a filtered bpsk with a randomly generated sequence
@wave_views.route("/bpsk", methods=["GET"])
def get_bpsk():
    schema = BPSKSchema()
    i=0
    try:
        data = schema.load(request.args)
        final_pulse = np.empty(0)
        for __ in range(data["num_pulses"]):
            single_pulse = generate_fbpsk(data["cutoff_freq"], data["num_taps"],data["num_bits"], data["sample_rate"], data["bit_length"], data["sequence_type"], data["pulse_reps"], data["num_pulses"])
            single_pulse = get_pulse_blanks(single_pulse, data["num_pulses"], data["amplitude"], data["pulse_reps"], data["sample_rate"], 1, "bpsk")
            final_pulse = np.append(final_pulse,single_pulse)
        return output_cases(final_pulse, data["form"], data["sample_rate"], "bpsk", data["axes"], data["num_pulses"], True) 

    except ValidationError as err:
        return {"errors": err.messages}, 400

#Returns the pulse with blanks spaces according
def get_pulse_blanks(pulse, num_pulses, amplitude, pri, sample_rate, pulse_width, wave_type):
    pulse = np.round(amplitude * pulse)
    if wave_type == "cw":
        samples_per_pulse = round(pulse_width * sample_rate)
        samples_per_pri = round(pri*sample_rate)
        buffer_samples = np.tile(0, max(0, samples_per_pri-samples_per_pulse)) #append this many 0s to get pri = pw + len(0s)
    elif wave_type == "lfm":
        samples_per_pulse = len(pulse)
        samples_per_pri = round(pri*sample_rate)
        buffer_samples = np.tile(0, max(0, samples_per_pri-samples_per_pulse))
    elif wave_type == "bpsk":
        samples_per_pulse = len(pulse) #get the length of a filtered pulse
        samples_per_pri = pri*sample_rate 
        buffer_samples = max(0, samples_per_pri-samples_per_pulse)
    pulse = np.append(pulse, buffer_samples) #add the zeros onto the pulse

    return pulse
