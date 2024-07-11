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

#crete graphs when button is pressed

@app.callback(
    #Output(graphs_display, component_property='figure'),
    Output("show_selected" , component_property = "children"),
    State(select_type_options, component_property='value'),
    Input("show_wave", component_property='n_clicks'), 
    State("gen_inputs", component_property='children')
    #State[(id for i in inp_list)]
)
def forms_redirection(select_type_options, n_clicks, children):
    #depending on button pressed, would want a dif graph output
    if select_type_options == "Continuous Wave": 
        print("in continuous wave")
        print("printtte")
        child = children[0]
        print(child)
        return html.Div([child['type'] for child['props'] in child])
    if select_type_options == "Linear Frequency Modulated":
        print("in lfm")
    if select_type_options == "Binary Phase Shift Keying":
        print("in bpsk")
'''
[
    Sample outlook of a child
    {'children': [
                    {'props': {'children': 'Sample Rate (Hz):'}, 'type': 'Label', 'namespace': 'dash_html_components'}, 
                    {'props': {'id': 'sample_rate', 'value': '20e6'}, 'type': 'Input', 'namespace': 'dash_bootstrap_components'}, 
                    {'props': {'children': 'Pulse Width (s):'}, 'type': 'Label', 'namespace': 'dash_html_components'}, 
                    {'props': {'id': 'pw', 'value': '10e-6'}, 'type': 'Input', 'namespace': 'dash_bootstrap_components'}, 
                    {'props': {'children': 'Pulse Repetition Interval (s):'}, 'type': 'Label', 'namespace': 'dash_html_components'}, 
                    {'props': {'id': 'signal_length', 'value': '20e-6'}, 'type': 'Input', 'namespace': 'dash_bootstrap_components'}, 
                    {'props': {'children': 'Amplitude'}, 'type': 'Label', 'namespace': 'dash_html_components'}, 
                    {'props': {'id': 'amplitude', 'value': '2000'}, 'type': 'Input', 'namespace': 'dash_bootstrap_components'}
                ]
    }
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
                form_options,
                html.Br(),
                html.Center([
                    dbc.Button("Show Waveform", color="info", id="show_wave", style={'marginRight': '15px'}),
                    dbc.Button("Download .sc16", color ="info", id="download")
                    ])
            ], style={'marginTop': '1%'}),
        dbc.Col([
                html.Center(dcc.Markdown(children="##### Interactive Plot:")),
                html.Div(graphs_display),
                html.Br(),
                html.Center(dcc.Markdown(children="##### 3-Dimensional Representation:")),
                html.Div(three_dim_graph)]),
                html.Center(html.P(id="show_selected", children= '')),
    ]),

])

if __name__ == "__main__":
   app.run(port=5000, debug=True)
   # app.run_server(port=5000, debug=True) #default into original webpage
