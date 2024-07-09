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


#variables

page_title = dcc.Markdown(children = '# Waveform Visualization')
graphs_display = dcc.Graph(figure={}) #nothing in graph in the beginning

select_type_options = dcc.RadioItems(
    create_radio_list(), value='Continuous Wave'
)


#layout of the form
form_options = html.Div([
        dcc.Markdown(children= '### Select Wave Type:'),
        select_type_options,
        html.Br(),
        dcc.Markdown(children="### Inputs:")
    ])