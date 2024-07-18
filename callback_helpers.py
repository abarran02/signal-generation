from views.views import get_lfm, get_bpsk, get_cw
from dash import no_update, ctx

#functions for callbacks in app.py (moved for clarity)
def populate_graphs(select_type_options, b1, b2, b3, b4, seq_type, num_bits, cutoff_freq, num_taps, children):
    triggered_id = ctx.triggered_id #determines which button was pressed 
    values = {} #dictionary of all input ids to values 
    #assign values from children and func depending on which wave form is inputted
    if select_type_options == "Continuous Wave": 
        children = children[0]['props']['children']
        create_vals_from_forms(children, values)
        wave_func = get_cw
    elif select_type_options == "Linear Frequency Modulated":
        children = children['props']['children']
        create_vals_from_forms(children, values)
        wave_func = get_lfm
    elif select_type_options == "Binary Phase Shift Keying":
        children = children['props']['children']
        create_vals_from_forms(children, values)
        create_vals_for_bpsk(values, seq_type, num_bits, cutoff_freq, num_taps)
        wave_func = get_bpsk
    return populate_graphs_from_trigger(triggered_id, values, wave_func)
    
def populate_graphs_from_trigger(triggered_id, values, wave_func): 
    if triggered_id == 'show_wave':
        #value output: {'sample_rate': '20e6', 'pw': '10e-6', 'signal_length': '20e-6', 'amplitude': '2000'}
        return wave_func(values, "graph", ""), wave_func(values, "threeDim", "default") #no_update
    elif triggered_id == 'real_z':
        return no_update, wave_func(values, "threeDim", "real_z")
    elif triggered_id == 'imag_z':
        return no_update, wave_func(values, "threeDim", "imag_z")
    elif triggered_id == 'imag_real':
        return no_update, wave_func(values, "threeDim", "imag_real")
    
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