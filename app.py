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

#dash tests
app = Dash(server=server, external_stylesheets=[dbc.themes.SLATE], prevent_initial_callbacks=True, suppress_callback_exceptions=True)


#Create rest of the form based on wave type selected 
@app.callback(
    Output("gen_inputs", component_property='children'),
    Input(select_type_options, component_property='value')
)
def format_inputs_list(select_type_options):
    return dbc.Col(generate_inputs_list(select_type_options))

#crete graphs when button is pressed
@app.callback(
    Output(graphs_display, component_property='figure'),
    Input("interactive_graph", component_property='value'), #form option should probably be something else
   # State()
)
def forms_redirection():
    #depending on button pressed, would want a dif graph output
    return 



#form and graphs laid out together
app.layout = dbc.Container([
    html.Center(page_title),
    html.Br(),
    dbc.Row([
        dbc.Col([
                html.Br(),
                form_options,
                html.Br(),
                html.Center([
                    dbc.Button("Show Waveform", color="info", id="showWave", style={'marginRight': '15px'}),
                    dbc.Button("Download .sc16", color ="info", id="download")
                    ])
            ], style={'marginTop': '1%'}),
        dbc.Col([
                html.Center(dcc.Markdown(children="##### Interactive Plot:")),
                html.Div(graphs_display),
                html.Br(),
                html.Center(dcc.Markdown(children="##### 3-Dimensional Representation:")),
                html.Div(three_dim_graph)]),
    ]),

])

if __name__ == "__main__":
   app.run(port=5000, debug=True)
   # app.run_server(port=5000, debug=True) #default into original webpage
