from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from flask import Blueprint, request, send_file
from marshmallow import ValidationError

import signal_utils as su
from signal_utils.common.binary_file_ops import get_iq_bytes

from .schema import *

wave_views = Blueprint("wave_views", __name__, url_prefix="/generate")

@wave_views.route("/cw", methods=["GET"])
def get_cw():
    schema = CWSchema()

    try:
        data = schema.load(request.args)
        pulse = su.continuous_wave.generate_cw_iq(data["frequency"], data["pulse_width"], data["pri"], data["num_reps"], data["sample_rate"])

        if data["form"] == "sc16":
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

        elif data["form"] == "png":
            t = np.linspace(0, data["pulse_width"], pulse.shape[0])
            buf = BytesIO()
            plt.figure()
            plt.plot(t, np.real(pulse), label="In-phase (I)")
            plt.plot(t, np.imag(pulse), label="Quadrature (Q)", linestyle="--")
            plt.title("Radar Signal in Time Domain")
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")

            plt.savefig(buf, format="png")
            buf.seek(0)
            return send_file(
                buf,
                mimetype="image/png"
            )

    except ValidationError as err:
        return {"errors": err.messages}, 400
