import json
from dash import Dash, html, dcc, Output, Input #gives interactivity
import dash_bootstrap_components as dbc

forms_json = "templates/forms.json"
name = "hey"

#reading json file
with open(forms_json, "r") as f: 
    forms = json.load(f)

def create_radio_list():
    radio_options = []
    for f in forms:
        radio_options.append(f['name'])
    return radio_options

def generate_inputs_list(selected_type):
    inp_lst = []
    for f in forms:
        if (f["name"] == selected_type):
            inputs = f #retrieve type from json file
            inputs = inputs['fields']
    for inp in inputs:
        '''
        if(inp["label"]!= "Sequencing Type:"):
            inp_options = inp["label"]
            inp_lst.append(dcc.Dropdown(inp_options["label"] for i in inp_options))
        else:
        '''
        inp_lst.append(html.Label(inp["label"]))
        inp_lst.append(dbc.Input(value=inp["value"], id=inp["name"]))
    return inp_lst

#variables

page_title = dcc.Markdown(children = '# Waveform Visualization')
graphs_display = dcc.Graph(figure={}) #nothing in graph in the beginning

select_type_options = dcc.RadioItems(
    create_radio_list(), value='Continuous Wave', style={'font-size': '18px', 'margin-left': '5'}
)

