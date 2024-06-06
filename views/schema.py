from marshmallow import Schema, fields, ValidationError

class ListField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, str):
            raise ValidationError("Invalid input type, must be a string")
        try:
            values = [int(x.strip()) for x in value.split(",")]
        except ValueError:
            raise ValidationError("Invalid list format, must be comma-separated integers")
        return values

class CWSchema(Schema):
    sample_rate = fields.Integer(required=True)
    signal_length = fields.Float(required=True)
    form = fields.String(required=True)

class PWSchema(Schema):
    sample_rate = fields.Integer(required=True)
    bit_length = fields.Float(required=True)
    num_bits = fields.Integer(required=True)
    taps = ListField(required=True)
    amplitude = fields.Integer(required=True)
    pri = fields.Float(required=True)
    num_pulses = fields.Integer(required=True)
    form = fields.String(required=True)

class LFMSchema(Schema):
    sample_rate = fields.Integer(required=True)
    fstart = fields.Float(required=True)
    fstop = fields.Float(required=True)
    signal_length = fields.Float(required=True)
    form = fields.String(required=True)
