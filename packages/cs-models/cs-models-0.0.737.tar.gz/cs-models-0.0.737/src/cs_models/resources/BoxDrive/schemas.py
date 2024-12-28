from marshmallow import (
    Schema,
    fields,
)


class BoxDriveResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    org_id = fields.String(allow_none=True)
    webhook_id = fields.String(required=True)
    updated_at = fields.DateTime(dump_only=True)
