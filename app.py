
from signal_utils import continuous_wave
from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError

app = Flask(__name__)

class CWSchema(Schema):
    frequency = fields.Float(required=True)
    pulse_width = fields.Float(required=True)
    pri = fields.Float(required=True)
    num_reps = fields.Integer(required=True)
    sample_rate = fields.Integer(required=True)

@app.route("/cw", methods=["GET"])
def get_cw():
    schema = CWSchema()

    try:
        data = schema.load(request.args)
        pulse = continuous_wave.generate_cw_iq(data["frequency"], data["pulse_width"], data["pri"], data["num_reps"], data["sample_rate"])

        return jsonify({
            "real": pulse.real.tolist(),
            "imag": pulse.imag.tolist()
        })

    except ValidationError as err:
        return {"errors": err.messages}, 400

if __name__ == "__main__":
    app.run(port=5000)
