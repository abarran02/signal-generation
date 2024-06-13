from marshmallow import Schema, ValidationError, fields, validate


class ScientificNotation(fields.Field):
    """Field that serializes to a string and deserializes
    to a floating point number.

    :param value_type: Specifies whether the field handles 'int' or 'float'. Defaults to 'int'.
    :type value_type: str, optional
    :param kwargs: Additional keyword arguments passed to the base Field class.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value_type = kwargs.get("value_type", "float")

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""

        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            if self.value_type == "int":
                # explicit cast to float because int(1e6) is invalid
                return int(float(value))

            return float(value)

        except ValueError as error:
            raise ValidationError("Invalid conversion to scientific notation.") from error

class WaveGeneric(Schema):
    sample_rate = ScientificNotation(value_type="int", required=True)
    form = fields.String(required=True, validate=validate.OneOf(["sc16", "png", "graph", "threeDim"]))
    axes = fields.String(missing=None, validate=validate.OneOf(["iqvt", "ivq"]))
    amplitude = ScientificNotation(value_type="int", required=True)

class CWSchema(WaveGeneric):
    signal_length = ScientificNotation(required=True)
    pw = ScientificNotation(required=True)

class LFMSchema(WaveGeneric):
    fstart = ScientificNotation(required=True)
    fstop = ScientificNotation(required=True)
    signal_length = ScientificNotation(required=True)
    num_pulses = ScientificNotation(value_type="int", required=True)
    pulse_reps = ScientificNotation(value_type="int", required=True)
    pw = ScientificNotation(required=True)

class BPSKSchema(WaveGeneric):
    bit_length = ScientificNotation(required=True)
    num_pulses = ScientificNotation(value_type="int", required=True)
    pulse_reps = ScientificNotation(value_type="int", required=True)
    sequence_type = fields.String(required=True, validate=validate.OneOf(["barker", "mls"]))
    num_bits = ScientificNotation(value_type="int", required=True)
    cutoff_freq = ScientificNotation(required=True)
    num_taps = ScientificNotation(value_type="int", required=True)
