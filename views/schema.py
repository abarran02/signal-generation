from marshmallow import Schema, fields


class CWSchema(Schema):
    frequency = fields.Float(required=True)
    pulse_width = fields.Float(required=True)
    pri = fields.Float(required=True)
    num_reps = fields.Integer(required=True)
    sample_rate = fields.Integer(required=True)
    form = fields.String(required=True)
