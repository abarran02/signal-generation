import json
from dash import Dash, html, dcc, Output, Input #gives interactivity
from views import * 
import dash_bootstrap_components as dbc

from views.views import get_cw

forms_json = "templates/forms.json"

#reading json file
with open(forms_json, "r") as f: 
    forms = json.load(f)

#take forms.json parameters and format it as a list to be created as a Dash Component
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
        curr_label = inp["label"]
        if (curr_label == "Sequencing Type:" or curr_label == "Number of Bits:"):
            continue
        else:
            inp_lst.append(html.Label(inp["label"], style={'marginBottom': '5px', 'fontSize': '18px'}))
            inp_lst.append(dbc.Input(value=inp["value"], id=inp["name"], style={'marginBottom': '15px'}))
    return inp_lst

#variable assignments

page_title = dcc.Markdown(children = '# Waveform Visualization')
graphs_display = dcc.Graph(figure={}, id="interactive_graph") #nothing in graph in the beginning
three_dim_graph = dcc.Graph(figure={}, id="three_dim", style={'marginBottom': '30px'})

select_type_options = dcc.RadioItems(
    create_radio_list(), value='Continuous Wave', style={'fontSize': '18px', 'marginLeft': '10px', 'display': 'flex','justifyContent':'center', 'textAlign': 'center'}
)

#layout of the form (left component)
form_options = html.Div([
        html.Center(dcc.Markdown(children= '### Select Wave Type')),
        html.Br(),
        select_type_options,
        html.Br(),
        html.Center(dcc.Markdown(children="### Inputs")),
        dbc.Container(id="gen_inputs", children=[dbc.Col(generate_inputs_list("Continuous Wave"))]), #children is default value
        #dbc.Container(id="bpsk_dropdowns", children = []),
        #dbc.Container(id="mlsbarker", children=[]) #if type is bpsk, generate extra forms
    ])

bpsk_extras = html.Div([
            html.Label("Sequencing Type", style={'marginBottom': '5px', 'fontSize': '18px', 'marginLeft': '12px'}),
            dcc.Dropdown(options=[{"label": "Maximum Length Sequencing (MLS)", "value": "mls"},
                                {"label": "Barker Code", "value": "barker"}],     
                                    style={'color':'black', 'marginBottom': '15px', 'marginLeft': '7px', 'marginRight': '20px'},
                                    id="seq_type"),
            html.Label("Number of Bits:",style={'marginBottom': '5px', 'fontSize': '18px', 'marginLeft': '12px'}),
            dcc.Dropdown(options=[],     
                        style={'color':'black', 'marginBottom': '15px', 'marginLeft': '7px', 'marginRight': '20px'},
                        id="bit_count")
        ], id = "bpsk_div", style= {'display': 'none'})