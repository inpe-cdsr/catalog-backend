"""
Validator
"""

from cerberus import Validator
from werkzeug.exceptions import BadRequest


def login():
    return {
        'username': {"type": "string", "empty": False, "required": True},
        'password': {"type": "string", "empty": False, "required": True}
    }


def validate(data, type_schema):
    if data is None:
        raise BadRequest('Body is empty.')

    schema = eval('{}()'.format(type_schema))

    v = Validator(schema)

    if not v.validate(data):
        return v.errors, False

    return data, True
