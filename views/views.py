from datetime import datetime
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from flask import Blueprint, request, send_file
from marshmallow import ValidationError
from numpy.typing import NDArray

import signal_utils as su
from signal_utils.common.binary_file_ops import get_iq_bytes
from signal_utils.common.sequences import maximal_length_sequence

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
            return send_bytes_response(pulse_bytes, "cw")

        elif data["form"] == "png":
            t = np.linspace(0, data["pulse_width"], pulse.shape[0])
            return send_plot_image(pulse, t)

    except ValidationError as err:
        return {"errors": err.messages}, 400

@wave_views.route("/pw", methods=["GET"])
def get_pw():
    schema = PWSchema()

    try:
        data = schema.load(request.args)
        seq = maximal_length_sequence(data["num_bits"], np.array(data["taps"]))
        pulse = su.radar_pulse.generate_pulse(seq, data["sample_rate"], data["bit_length"], data["pri"], data["num_pulses"])
        pulse = np.round(data["amplitude"] * pulse)

        if data["form"] == "sc16":
            pulse_bytes = get_iq_bytes(pulse)
            return send_bytes_response(pulse_bytes, "pw")

        elif data["form"] == "png":
            t = np.linspace(0, data["bit_length"], pulse.shape[0])
            return send_plot_image(pulse, t)

    except ValidationError as err:
        return {"errors": err.messages}, 400

@wave_views.route("/lfm", methods=["GET"])
def get_lfm():
    schema = LFMSchema()

    try:
        data = schema.load(request.args)
        pulse = su.linear_frequency_modulated.generate_lfm(data["sample_rate"], data["fstart"], data['fstop'], data["signal_length"])

        if data["form"] == "sc16":
            pulse_bytes = get_iq_bytes(pulse)
            return send_bytes_response(pulse_bytes, "lfm")

        elif data["form"] == "png":
            t = np.linspace(0, data["signal_length"], pulse.shape[0])
            return send_plot_image(pulse, t)

    except ValidationError as err:
        return {"errors": err.messages}, 400

def send_bytes_response(pulse_bytes: bytes, prefix: str):
    # get current time for file naming
    now = datetime.now()
    formatted_time = now.strftime("%Y%m%d_%H%M%S")

    return send_file(
        BytesIO(pulse_bytes),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name=f"{prefix}_{formatted_time}.sc16"
    )

def send_plot_image(pulse: NDArray[np.complex_], t: NDArray[np.float_]):
    buf = BytesIO()
    plt.figure()
    plt.plot(t, np.real(pulse), label="In-phase (I)")
    plt.plot(t, np.imag(pulse), label="Quadrature (Q)", linestyle="--")
    plt.title("Radar Signal in Time Domain")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()

    plt.savefig(buf, format="png")
    buf.seek(0)
    return send_file(
        buf,
        mimetype="image/png"
    )
