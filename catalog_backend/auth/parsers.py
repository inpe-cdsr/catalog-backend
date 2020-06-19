"""
Validator
"""

from cerberus import Validator


def login():
    return {
        'email': {"type": "string", "empty": False, "required": True},
        'password': {"type": "string", "empty": False, "required": True}
    }


def validate(data, type_schema):
    schema = eval('{}()'.format(type_schema))

    v = Validator(schema)

    if not v.validate(data):
        return v.errors, False

    return data, True
