from marshmallow import Schema, fields


class UsersSchema(Schema):

    username = fields.String(required=True)
    password = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.Email(required=True)
    roles = fields.List(fields.String(), required=True)


class UpdateUsersSchema(Schema):

    username = fields.String(required=False)
    password = fields.String(required=False)
    phone = fields.String(required=False)
    email = fields.Email(required=False)
    roles = fields.List(fields.String(), required=False)
