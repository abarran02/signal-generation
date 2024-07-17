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
def get_cw(data, form):
    schema = CWSchema()

    try:
        data["form"] = form #hardcoded to 2d interactive for now
        data["axes"] = '' #dummy param
        data = schema.dump(data)
        convert_cw_types(data)
        pulse = su.continuous_wave.generate_cw(data["sample_rate"], data["pw"])
        pulse = get_pulse_blanks(pulse, 1, data["amplitude"], data["signal_length"], data["sample_rate"], data["pw"], "cw")

        return output_cases(pulse, data["form"], data["signal_length"], "CW", data["axes"], 1, False)

    except ValidationError as err:
        return {"errors": err.messages}, 400
def convert_generic_inputs(data):
    data["sample_rate"] = float(data["sample_rate"])
    data["amplitude"] = int(data["amplitude"])   
    
def convert_cw_types(data):
    convert_generic_inputs(data)
    data["signal_length"] = float(data["signal_length"])
    data["pw"] = float(data["pw"])


@wave_views.route("/lfm", methods=["GET"])
def get_lfm(data, form):
    schema = LFMSchema()
    try:
        data["form"] = form #hardcoded to 2d interactive for now
        data["axes"] = '' #dummy param
        data = schema.dump(data)
        convert_lfm_types(data)
        pulse = su.linear_frequency_modulated.generate_lfm(data["sample_rate"], data["fstart"], data['fstop'], data["pw"], data["num_pulses"])
        pulse = get_pulse_blanks(pulse, data["num_pulses"], data["amplitude"], data["pri"], data["sample_rate"],  data["pw"], "lfm")
        pulse = np.tile(pulse, data["num_pulses"])

        return output_cases(pulse, data["form"], data["pri"], "lfm", data["axes"], data["num_pulses"],False)
    except ValidationError as err:
        return {"errors": err.messages}, 400  

def convert_lfm_types(data):
    convert_generic_inputs(data)
    data["fstart"] = float(data['fstart'])
    data["fstop"] = float(data['fstop'])
    data['num_pulses'] = int(data['num_pulses'])
    data['pw'] = float(data['pw'])
    data['pri'] = float(data['pri'])

#For each pulse, create a filtered bpsk with a randomly generated sequence
@wave_views.route("/bpsk", methods=["GET"])
def get_bpsk(data, form):
    schema = BPSKSchema()
    try:
        print("data")
        print(data['num_bits'])
        data["form"] = form #hardcoded to 2d interactive for now
        data["axes"] = '' #dummy param
        #data = schema.dump(data)
        convert_bpsk_types(data)
        print("converted bpsk")
        final_pulse = np.empty(0)
        num_bit = data["num_bits"]
        for __ in range(data["num_pulses"]):
            single_pulse = generate_fbpsk(data["cutoff_freq"], data["num_taps"], num_bit, data["sample_rate"], data["bit_length"], data["seq_type"], data["pulse_reps"], data["num_pulses"])
            single_pulse = get_pulse_blanks(single_pulse, data["num_pulses"], data["amplitude"], data["pulse_reps"], data["sample_rate"], 1, "bpsk")
            final_pulse = np.append(final_pulse,single_pulse)
        print("output cases bpsk")
        return output_cases(final_pulse, data["form"], data["pulse_reps"], "bpsk", data["axes"], data["num_pulses"], True) 

    except ValidationError as err:
        return {"errors": err.messages}, 400
def convert_bpsk_types(data):
    convert_generic_inputs(data)
    data["bit_length"] = float(data["bit_length"])
    data["num_pulses"] = int(data["num_pulses"])
    data["pulse_reps"] = float(data['pulse_reps'])
    data["cutoff_freq"] = int(data["cutoff_freq"])
    data["num_taps"] = int(data["num_taps"])

#Returns the pulse with blanks spaces according
def get_pulse_blanks(pulse, num_pulses, amplitude, pri, sample_rate, pulse_width, wave_type):
    pulse = np.round(amplitude * pulse)
    if wave_type == "cw":
        samples_per_pulse = round(pulse_width * sample_rate)
        samples_per_pri = round(pri*sample_rate)
        buffer_samples = np.zeros(max(0, int(samples_per_pri-samples_per_pulse))) #append this many 0s to get pri = pw + len(0s)
    elif wave_type == "lfm":
        samples_per_pulse = round(pulse_width*sample_rate)
        samples_per_pri = round(pri*sample_rate)
        buffer_samples = np.zeros(max(0, int(samples_per_pri-samples_per_pulse)))
    elif wave_type == "bpsk":
        samples_per_pulse = len(pulse) #get the length of a filtered pulse
        samples_per_pri = pri*sample_rate 
        buffer_samples = np.zeros(max(0, int(samples_per_pri-samples_per_pulse)))
    pulse = np.append(pulse, buffer_samples) #add the zeros onto the pulse

    return pulse
