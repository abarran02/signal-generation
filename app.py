from flask import Flask, render_template
from views import wave_views

app = Flask(__name__)
app.register_blueprint(wave_views)

@app.route('/')
def index():
    html_file = "index.html"
    return render_template(html_file)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
