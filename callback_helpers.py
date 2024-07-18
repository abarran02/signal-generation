from views.views import get_lfm, get_bpsk, get_cw

#functions for callbacks in app.py (moved for clarity)

def populate_graphs(select_type_options, seq_type, num_bits, cutoff_freq, num_taps, children):
    values = {} #dictionary of all input ids to values 
    if select_type_options == "Continuous Wave": 
        children = children[0]['props']['children']
        create_vals_from_forms(children, values)
        #value output: {'sample_rate': '20e6', 'pw': '10e-6', 'signal_length': '20e-6', 'amplitude': '2000'}
        return get_cw(values, "graph", ""), get_cw(values, "threeDim", "default")
    
    elif select_type_options == "Linear Frequency Modulated":
        children = children['props']['children']
        create_vals_from_forms(children, values)
        return get_lfm(values, "graph", ""), get_lfm(values, "threeDim", "default")
    
    elif select_type_options == "Binary Phase Shift Keying":
        children = children['props']['children']
        create_vals_from_forms(children, values)
        create_vals_for_bpsk(values, seq_type, num_bits, cutoff_freq, num_taps)
        return get_bpsk(values, "graph", ""), get_bpsk(values, "threeDim", "default")
    
#populate values (dictionary of all input ids to form values)
def create_vals_from_forms(children, values):
    for child in children:
        dict = child['props']
        if 'id' in dict.keys():
            id_value = dict['id']
            value = dict['value']
            values[id_value] = value

#adds additional bpsk inputs into the values dictionary
def create_vals_for_bpsk(values, seq_type, num_bits, cutoff_freq, num_taps):
    values["seq_type"] = seq_type
    values["num_bits"] = num_bits
    values["cutoff_freq"] = cutoff_freq
    values["num_taps"] = num_taps

def download_wave_helper(select_type_options, n_clicks, seq_type, num_bits, cutoff_freq, num_taps, children):
    values = {} #dictionary of all input ids to values 
    if select_type_options == "Continuous Wave": 
        children = children[0]['props']['children']
        create_vals_from_forms(children, values)
        return get_cw(values, "sc16", "")
    
    elif select_type_options == "Linear Frequency Modulated":
        children = children['props']['children']
        create_vals_from_forms(children, values)
        return get_lfm(values, "sc16", "")
    
    elif select_type_options == "Binary Phase Shift Keying":
        children = children['props']['children']
        create_vals_from_forms(children, values)
        create_vals_for_bpsk(values, seq_type, num_bits, cutoff_freq, num_taps)
        return get_bpsk(values, "sc16", "")