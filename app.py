import json
import plotly.graph_objs as go

from dash import Dash, html, dcc, Output, Input, State #gives interactivity
import dash_bootstrap_components as dbc
from flask import Flask, render_template

from views import wave_views
from views.views import get_lfm, get_bpsk
from formfuncs import *
from callback_helpers import *

server = Flask(__name__)
server.register_blueprint(wave_views)

@server.route('/')
def index():
    html_template = "index.jinja"
    forms_json = "templates/forms.json"
    
    with open(forms_json, "r") as f:
        forms = json.load(f)

    return render_template(html_template, forms=forms)

#Dash app (accessible by adding /dash/ to end of generated url)
app = Dash(server=server, external_stylesheets=[dbc.themes.SLATE], prevent_initial_callbacks=True, suppress_callback_exceptions=True)

### FORM GENERATION CALLBACKS ###

#Create rest of the form based on wave type selected 
@app.callback( 
    Output("gen_inputs", component_property='children'),
    Input(select_type_options, component_property='value')
)
def format_inputs_list(select_type_options):
    curr_option = select_type_options
    return dbc.Col(generate_inputs_list(curr_option))

#changes visibility of sequencing type options depending on waveform type
@app.callback(
        Output("bpsk_div", component_property='style'),
        Input(select_type_options, component_property='value'))
def create_bpsk_dropdown(select_type_options):
    if select_type_options == "Binary Phase Shift Keying":
        return {'display': 'block'}
    else:
        return {'display': 'none'}

#Creates the number of bits based on which seq_type is selected
@app.callback(
        Output("num_bits", "options"),
        Input("seq_type", "value"))
def create_dropdown(seq_type):
    mls_options = [4, 5, 6, 7, 8, 9]
    barker_options = [2, 3, 4, 5, 7, 11, 13]
    if(seq_type == "mls"):
        return mls_options
    else:
        return barker_options
    
### POPULATING GRAPH CALLBACK ###
    
#crete corresponding waveform graphs when button is pressed
@app.callback(
    Output("interactive_graph" , component_property= 'children'),
    Output("three_dim_graph" , component_property= 'children'),

    State(select_type_options, component_property='value'),

    Input("show_wave", component_property='n_clicks'), 
    Input("real_z", component_property='n_clicks'), 
    Input("imag_z", component_property='n_clicks'),
    Input("imag_real", component_property='n_clicks'),

    State("seq_type", "value"),
    State("num_bits", "value"),
    State("cutoff_freq", "value"),
    State("num_taps", "value"),
    State("gen_inputs", component_property='children'),

    prevent_initial_call=True
)
def forms_redirection(select_type_options, b1, b2, b3, b4, seq_type, num_bits, cutoff_freq, num_taps, children):
    return populate_graphs(select_type_options, seq_type, num_bits, cutoff_freq, num_taps, children)

### CONTROL GRAPH CAMERA ANGLES ###

#display a top view
'''
@app.callback(
    Output("tester", 'children'),
    Input("three_dim_graph", component_property='children'),
    State(select_type_options, component_property='value'),
    Input("real_z", component_property='n_clicks'),
    prevent_initial_call=True
)
def update_real_z(children, options, n_clicks):
    values = {} #dictionary of all input ids to values 
    #children = children[0]['props']['children']
    create_vals_from_forms(children, values)
    return get_cw(values, "threeDim", "real_z")
'''



### DOWNLOAD CALLBACK ###

#given the selected waveform type, download to corresponding .sc16 file when button is pressed 
@app.callback(
    Output("download-sc16", component_property='data'),
    State(select_type_options, component_property='value'),
    Input("download", component_property='n_clicks'), 
    State("seq_type", "value"),
    State("num_bits", "value"),
    State("cutoff_freq", "value"),
    State("num_taps", "value"),
    State("gen_inputs", component_property='children')
)
def download_wave(select_type_options, n_clicks, seq_type, num_bits, cutoff_freq, num_taps, children):
    return download_wave_helper(select_type_options, n_clicks, seq_type, num_bits, cutoff_freq, num_taps, children)

    
#form and graphs laid out together
app.layout = dbc.Container([
    html.Br(),
    html.Center(page_title),
    html.Br(),
    dbc.Row([
        dbc.Col([
                html.Br(),
                html.Div([
                    form_options,
                    bpsk_extras,
                ], style={'color': '#E9E8F2','backgroundColor':'#59585F', 'padding': '1.5rem 1rem', 'borderRadius': '10px'}),
                html.Br(),
                html.Center([
                    dbc.Button("Show Waveform", color="info", id="show_wave", style={'marginRight': '15px'}),
                    dbc.Button("Download .sc16", color ="info", id="download"),
                    dcc.Download(id="download-sc16")
                    ])
            ], style={'marginTop': '1%', 'width': '20%'}),
        dbc.Col([
                html.Center(dcc.Markdown(children="##### Interactive Plot:")),
                html.Div(id="interactive_graph", children = [dcc.Graph(figure={}, id="interactive", style={'marginBottom': '30px'})]),
                html.Br(),
                html.Center(dcc.Markdown(children="##### Three-Dimensional Representation:")),
                html.Div(id="three_dim_graph", children = [dcc.Graph(figure={}, id="three_dim", style={'marginBottom': '30px'})]),
                html.Center([
                    dbc.Button("Imaginary-Z", color="secondary", id="imag_z", style={'marginRight': '5px'}),
                    dbc.Button("Real-Z", color="secondary", id="real_z", style={'marginRight': '5px'}),
                    dbc.Button("Imaginary-Real", color="secondary", id="imag_real"), #top view
                    html.P(id = "tester", children=[]),
                ]),
                html.Br()
                ], style = {'width': '80%'})
    ]),

])

if __name__ == "__main__":
   app.run(port=5000, debug=True)
   #app.run_server(port=5000, debug=True) #default into original webpage
