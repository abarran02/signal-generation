import numpy as np
from flask import Blueprint, request
from marshmallow import ValidationError

import signal_utils as su
from signal_utils.common.sequences import generate_fbpsk

from .response import output_cases
from .schema import *

wave_views = Blueprint("wave_views", __name__, url_prefix="/generate")

@wave_views.route("/cw", methods=["GET"])
def get_cw():
    schema = CWSchema()

    try:
        data = schema.load(request.args)
        pulse = su.continuous_wave.generate_cw(data["sample_rate"], data["signal_length"])
        pulse = get_pulse_blanks(pulse, 1, data["amplitude"], 1, 1, False)

        return output_cases(pulse, data["form"], data["signal_length"], "CW", data["axes"], 1, False)

    except ValidationError as err:
        return {"errors": err.messages}, 400

@wave_views.route("/lfm", methods=["GET"])
def get_lfm():
    schema = LFMSchema()

    try:
        data = schema.load(request.args)
        pulse = su.linear_frequency_modulated.generate_lfm(data["sample_rate"], data["fstart"], data['fstop'], data["pri"], data["num_pulses"])
        pulse = get_pulse_blanks(pulse, data["num_pulses"], data["amplitude"], data["pri"], 1, False)

        return output_cases(pulse, data["form"], data["pri"], "lfm", data["axes"], data["num_pulses"],False)

    except ValidationError as err:
        return {"errors": err.messages}, 400

@wave_views.route("/bpsk", methods=["GET"])
def get_bpsk():
    schema = BPSKSchema()
    try:
        data = schema.load(request.args)
        final_pulse = np.empty(0)
        for __ in range(data["num_pulses"]):
            single_pulse = generate_fbpsk(data["cutoff_freq"], data["num_taps"],data["num_bits"], data["sample_rate"], data["bit_length"], data["sequence_type"], data["pulse_reps"], data["num_pulses"])
            print("single_pulse")
            print(single_pulse)
            single_pulse = get_pulse_blanks(single_pulse, data["num_pulses"], data["amplitude"], data["pulse_reps"], data["sample_rate"], True)
            print("pulse reps")
            print(data["pulse_reps"] * data["sample_rate"])
            final_pulse = np.append(final_pulse,single_pulse)
        return output_cases(final_pulse, data["form"], data["sample_rate"], "bpsk", data["axes"], data["num_pulses"], True) 

    except ValidationError as err:
        return {"errors": err.messages}, 400

def get_pulse_blanks(pulse, num_pulses, amplitude, pri, sample_rate, is_bpsk):
    #returns the pulse with blanks spaces according to the number of pulses
    pulse = np.round(amplitude * pulse)
    if is_bpsk == True:
        samples_per_pulse = len(pulse) #get the length of a filtered pulse
        samples_per_pri = pri*sample_rate #for some reason, pri is 0, possibly
        buffer_samples = max(0, samples_per_pri-samples_per_pulse)
        pulse = np.append(pulse, buffer_samples)
    else:
        pulse = np.append(pulse, np.zeros(len(pulse)))
        pulse = np.tile(pulse, num_pulses)

    return pulse
