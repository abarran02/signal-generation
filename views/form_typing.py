#Change inputted parameters from string to their desired type

def convert_generic_inputs(data):
    data["sample_rate"] = float(data["sample_rate"])
    data["amplitude"] = int(data["amplitude"])   
    
def convert_cw_types(data):
    convert_generic_inputs(data)
    data["signal_length"] = float(data["signal_length"])
    data["pw"] = float(data["pw"])

def convert_lfm_types(data):
    convert_generic_inputs(data)
    data["fstart"] = float(data['fstart'])
    data["fstop"] = float(data['fstop'])
    data['num_pulses'] = int(data['num_pulses'])
    data['pw'] = float(data['pw'])
    data['pri'] = float(data['pri'])

def convert_bpsk_types(data):
    convert_generic_inputs(data)
    data["bit_length"] = float(data["bit_length"])
    data["num_pulses"] = int(data["num_pulses"])
    data["pulse_reps"] = float(data['pulse_reps'])
    data["cutoff_freq"] = int(data["cutoff_freq"])
    data["num_taps"] = int(data["num_taps"])