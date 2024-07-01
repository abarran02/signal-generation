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
        pulse = get_pulse_blanks(pulse, 1, data["amplitude"], False)

        return output_cases(pulse, data["form"], data["signal_length"], "CW", data["axes"], 1)

    except ValidationError as err:
        return {"errors": err.messages}, 400

@wave_views.route("/lfm", methods=["GET"])
def get_lfm():
    schema = LFMSchema()

    try:
        data = schema.load(request.args)
        pulse = su.linear_frequency_modulated.generate_lfm(data["sample_rate"], data["fstart"], data['fstop'], data["pri"], data["num_pulses"])
        pulse = get_pulse_blanks(pulse, data["num_pulses"], data["amplitude"],False)

        return output_cases(pulse, data["form"], data["pri"], "lfm", data["axes"], data["num_pulses"])

    except ValidationError as err:
        return {"errors": err.messages}, 400

@wave_views.route("/bpsk", methods=["GET"])
def get_bpsk():
    schema = BPSKSchema()
    try:
        data = schema.load(request.args)

        pulse = generate_fbpsk(data["cutoff_freq"], data["num_taps"],data["num_bits"], data["sample_rate"], data["bit_length"], data["sequence_type"], data["pulse_reps"], data["num_pulses"])
        
        pulse = get_pulse_blanks(pulse, data["num_pulses"], data["amplitude"], True)

        return output_cases(pulse, data["form"], data["bit_length"], "bpsk", data["axes"], data["num_pulses"]) #need to fix x-axis for bpsk

    except ValidationError as err:
        return {"errors": err.messages}, 400

def get_pulse_blanks(pulse, num_pulses, amplitude, is_bpsk):
    #returns the pulse with blanks spaces according to the number of pulses
    pulse = np.round(amplitude * pulse)
    if is_bpsk == True:
        pulse_with_zeros = np.append(pulse, np.zeros(len(pulse)))
    else:
        pulse_with_zeros = np.append(pulse, np.zeros(len(pulse)))
    pulse = np.tile(pulse_with_zeros, num_pulses)

    return pulse
