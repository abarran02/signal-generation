import json

from dash import Dash, html, dcc, Output, Input #gives interactivity
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



@app.callback(
    Output("gen_inputs", component_property='children'),
    Input(select_type_options, component_property='value')
)
def format_inputs_list(select_type_options):
    return dbc.Col(generate_inputs_list(select_type_options))


#layout of the form
form_options = html.Div([
        dcc.Markdown(children= '### Select Wave Type:'),
        select_type_options,
        html.Br(),
        dcc.Markdown(children="### Inputs:"),
        dbc.Container(id="gen_inputs", children=[]),
        #input the buttons heres
    ])
'''
@app.callback(
    Output(graphs_display, component_property='figure'),
    Input(form_options, component_property='value') #form option should probably be something else
)
def forms_redirection():
    #depending on button pressed, would want a dif graph output
    print('hey')

'''


#form and graphs laid out together
app.layout = dbc.Container([
    html.Center(page_title),
    html.Br(),
    dbc.Row([
        dbc.Col([form_options]),
        dbc.Col(html.Div(graphs_display)),
    ])
])

if __name__ == "__main__":
   app.run(port=5000, debug=True)
   # app.run_server(port=5000, debug=True) #default into original webpage
