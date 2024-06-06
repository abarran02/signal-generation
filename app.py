from datetime import datetime
from io import BytesIO

from flask import Flask, request, send_file
from marshmallow import Schema, ValidationError, fields

import signal_utils as su
from signal_utils.common.binary_file_ops import get_iq_bytes

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
        pulse = su.continuous_wave.generate_cw_iq(data["frequency"], data["pulse_width"], data["pri"], data["num_reps"], data["sample_rate"])
        pulse_bytes = get_iq_bytes(pulse)

        # get current time for file naming
        now = datetime.now()
        formatted_time = now.strftime("%Y%m%d_%H%M%S")

        return send_file(
            BytesIO(pulse_bytes),
            mimetype="application/octet-stream",
            as_attachment=True,
            download_name=f"cw_{formatted_time}.sc16"
        )

    except ValidationError as err:
        return {"errors": err.messages}, 400

if __name__ == "__main__":
    app.run(port=5000)
