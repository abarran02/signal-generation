import json
from dash import html, dcc #gives interactivity
from views import * 
import dash_bootstrap_components as dbc

from views.views import get_cw

forms_json = "templates/forms.json"

#reading json file
with open(forms_json, "r") as f: 
    forms = json.load(f)

#take forms.json parameters and format it as a list to be created as a Dash Component in app.py
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
            inp_lst.append(html.Label(inp["label"], style={'marginBottom': '5px'}))
            inp_lst.append(dbc.Input(value=inp["value"], id=inp["name"], style={'marginBottom': '15px'}))
    return inp_lst

#variable assignments

page_title = dcc.Markdown(children = '# Waveform Visualization')

select_type_options = dcc.RadioItems(
    create_radio_list(), value='Continuous Wave', style={'fontSize': '20px', 'marginLeft': '10px','justifyContent':'center', 'textAlign': 'center', 'padding': '10px'}
)

#layout of the form (left component)
form_options = html.Div([
        html.Center(dcc.Markdown(children= '### Select Wave Type')),
        html.Br(),
        select_type_options,
        html.Br(),
        html.Center(dcc.Markdown(children="### Inputs")),
        dbc.Container(id="gen_inputs", children=[dbc.Col(generate_inputs_list("Continuous Wave"))]), #children is default value
    ])

bpsk_extras = html.Div([
            html.Label("Sequencing Type", style={'marginBottom': '5px'}),
            dcc.Dropdown(options=[{"label": "Maximum Length Sequencing (MLS)", "value": "mls"},
                                {"label": "Barker Code", "value": "barker"}], 
                                style={'color':'black', 'marginBottom': '15px'},
                                id="seq_type"),
            html.Label("Number of Bits:",style={'marginBottom': '5px'}),
            dcc.Dropdown(options=[],     
                        style={'color':'black', 'marginBottom': '15px'},
                        id="num_bits"),
            html.Center(dcc.Markdown(children="### Filtering")),
            dbc.Row([
                dbc.Col([
                    html.Label("Cutoff Frequency (Hz):"),
                    dbc.Input(value=20, id="cutoff_freq", style={'marginBottom': '15px'})
                ]),
                dbc.Col([
                    html.Label("Number of Taps:"),
                    dbc.Input(value=2, id="num_taps", style={'marginBottom': '15px'})
                ])
            ])
        ], id = "bpsk_div", style= {'display': 'none'})