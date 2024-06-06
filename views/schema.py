from marshmallow import Schema, fields


class CWSchema(Schema):
    frequency = fields.Float(required=True)
    pulse_width = fields.Float(required=True)
    pri = fields.Float(required=True)
    num_reps = fields.Integer(required=True)
    sample_rate = fields.Integer(required=True)
    form = fields.String(required=True)

class PWSchema(Schema):
    sample_rate = fields.Integer(required=True)
    bit_length = fields.Float(required=True)
    num_bits = fields.Integer(required=True)
    taps = fields.List(fields.Nested(fields.Integer), required=True)
    amplitude = fields.Integer(required=True)
    pri = fields.Float(required=True)
    num_pulses_pw = fields.Integer(required=True)

class LFMSchema(Schema):
    pulse_width_lfm = fields.Float(required=True)
    pri = fields.Float(required=True)
    num_reps = fields.Integer(required=True)
    fstart = fields.Integer(required=True)
    fstop = fields.Integer(required=True)
    sample_rate_lfm = fields.Integer(required=True)