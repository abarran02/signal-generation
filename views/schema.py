from marshmallow import Schema, fields


class CWSchema(Schema):
    sample_rate = fields.Integer(required=True)
    signal_length = fields.Float(required=True)
    form = fields.String(required=True)

class PWSchema(Schema):
    sample_rate = fields.Integer(required=True)
    bit_length = fields.Float(required=True)
    num_bits = fields.Integer(required=True)
    taps = fields.List(fields.Nested(fields.Integer), required=True)
    amplitude = fields.Integer(required=True)
    pri = fields.Float(required=True)
    num_pulses_pw = fields.Integer(required=True)
    form = fields.String(required=True)

class LFMSchema(Schema):
    sample_rate = fields.Integer(required=True)
    fstart = fields.Float(required=True)
    fstop = fields.Float(required=True)
    signal_length = fields.Float(required=True)
    form = fields.String(required=True)
