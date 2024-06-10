import json

from flask import Flask, render_template

from views import wave_views

app = Flask(__name__)
app.register_blueprint(wave_views)

@app.route('/')
def index():
    html_template = "index.jinja"
    forms_json = "templates/forms.json"

    with open(forms_json, "r") as f:
        forms = json.load(f)

    return render_template(html_template, forms=forms)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
