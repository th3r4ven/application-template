from marshmallow import Schema, fields


class RolesSchema(Schema):

    name = fields.String(required=True)
    users = fields.List(fields.String(), required=True)


class UpdateRolesSchema(Schema):

    name = fields.String(required=False)
    users = fields.List(fields.String(), required=False)
