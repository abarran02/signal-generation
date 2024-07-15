import json

from dash import Dash, html, dcc, Output, Input, State #gives interactivity
import dash_bootstrap_components as dbc
from flask import Flask, render_template
from formfuncs import *

from views import wave_views

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
        Output("bit_count", "options"),
        Input("seq_type", "value"))
def create_dropdown(seq_type):
    mls_options = [4, 5, 6, 7, 8, 9]
    barker_options = [2, 3, 4, 5, 7, 11, 13]
    if(seq_type == "mls"):
        return mls_options
    else:
        return barker_options
#crete corresponding waveform graphs when button is pressed
@app.callback(
    #Output(graphs_display, component_property='figure'),
    Output("interactive_graph" , component_property= 'children'),
    Output("three_dim_graph" , component_property= 'children'),
    State(select_type_options, component_property='value'),
    Input("show_wave", component_property='n_clicks'), 
    State("gen_inputs", component_property='children')
    #State[(id for i in inp_list)]
)
def forms_redirection(select_type_options, n_clicks, children):
    if select_type_options == "Continuous Wave": 
        values = {} #dictionary of all input ids to values 
        children = children[0]['props']['children']
        for child in children:
            dict = child['props']
            #print('dict')
            #print(dict)
            if 'id' in dict.keys():
                id_value = dict['id']
                value = dict['value']
                values[id_value] = value
                #value output: {'sample_rate': '20e6', 'pw': '10e-6', 'signal_length': '20e-6', 'amplitude': '2000'}
        return get_cw(values, "graph"), get_cw(values, "threeDim")
    if select_type_options == "Linear Frequency Modulated":
        print("in lfm")
        print(children)
    if select_type_options == "Binary Phase Shift Keying":
        print("in bpsk")
        print(children)
'''
Sample outlook of a child
[
    {'props': {'children': 'Sample Rate (Hz):', 'style': {'marginBottom': '5px'}}, 'type': 'Label', 'namespace': 'dash_html_components'}, 
    {'props': {'id': 'sample_rate', 'style': {'marginBottom': '15px'}, 'value': '20e6'}, 'type': 'Input', 'namespace': 'dash_bootstrap_components'}, 
    {'props': {'children': 'Pulse Width (s):', 'style': {'marginBottom': '5px'}}, 'type': 'Label', 'namespace': 'dash_html_components'}, 
    {'props': {'id': 'pw', 'style': {'marginBottom': '15px'}, 'value': '10e-6'}, 'type': 'Input', 'namespace': 'dash_bootstrap_components'}, 
    {'props': {'children': 'Pulse Repetition Interval (s):', 'style': {'marginBottom': '5px'}}, 'type': 'Label', 'namespace': 'dash_html_components'}, 
    {'props': {'id': 'signal_length', 'style': {'marginBottom': '15px'}, 'value': '20e-6'}, 'type': 'Input', 'namespace': 'dash_bootstrap_components'}, 
    {'props': {'children': 'Amplitude', 'style': {'marginBottom': '5px'}}, 'type': 'Label', 'namespace': 'dash_html_components'}, 
    {'props': {'id': 'amplitude', 'style': {'marginBottom': '15px'}, 'value': '2000'}, 'type': 'Input', 'namespace': 'dash_bootstrap_components'}]   
]     
'''


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
                    dbc.Button("Download .sc16", color ="info", id="download")
                    ])
            ], style={'marginTop': '1%'}),
        dbc.Col([
                html.Center(dcc.Markdown(children="##### Interactive Plot:")),
                html.Div(id="interactive_graph", children = [dcc.Graph(figure={}, id="interactive", style={'marginBottom': '30px'})]),
                html.Br(),
                html.Center(dcc.Markdown(children="##### Three-Dimensional Representation:")),
                html.Div(id="three_dim_graph", children = [dcc.Graph(figure={}, id="three_dim", style={'marginBottom': '30px'})]),
                html.Br()
                ])
    ]),

])

if __name__ == "__main__":
   app.run(port=5000, debug=True)
   # app.run_server(port=5000, debug=True) #default into original webpage
