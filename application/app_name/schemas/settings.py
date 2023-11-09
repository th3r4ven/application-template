from marshmallow import Schema, fields, validate


class SettingsSchema(Schema):

    log_level = fields.String(required=True, validate=validate.OneOf(
        [
            "notset", "debug", "info", "warn", "error", "critical"
        ]
    ))
