"""Schemas for input validation using Marshmallow."""

from marshmallow import Schema, fields, validate


# PUBLIC_INTERFACE
class RegisterSchema(Schema):
    """Schema for user registration."""
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=6))


# PUBLIC_INTERFACE
class LoginSchema(Schema):
    """Schema for login."""
    username = fields.Str(required=True)
    password = fields.Str(required=True)


# PUBLIC_INTERFACE
class EventSchema(Schema):
    """Schema for event validation."""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    date = fields.Str(
        required=True,
        validate=validate.Regexp(
            r'^\d{4}-\d{2}-\d{2}$', error="Date must be in YYYY-MM-DD format"
        ),
    )


# PUBLIC_INTERFACE
class EventUpdateSchema(Schema):
    """Schema for event update."""
    title = fields.Str(validate=validate.Length(min=1, max=120))
    description = fields.Str(validate=validate.Length(min=1, max=500))
    date = fields.Str(
        validate=validate.Regexp(
            r'^\d{4}-\d{2}-\d{2}$', error="Date must be in YYYY-MM-DD format"
        ),
    )
