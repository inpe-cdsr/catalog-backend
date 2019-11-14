"""
validation of controllers schemas
"""
from cerberus import Validator


def login():
    return {
        'username': {"type": "string", "empty": False, "required": True},
        'password': {"type": "string", "empty": False, "required": True}
    }


def validate(data, type_schema):
    schema = eval('{}()'.format(type_schema))

    v = Validator(schema)
    data_json = data.to_dict()

    if not v.validate(data_json):
        return v.errors, False

    return data, True
