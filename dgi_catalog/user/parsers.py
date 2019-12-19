"""
Validator
"""

from cerberus import Validator


INSERT_USER_SCHEMA = {
    'email': {"type": "string", "empty": False, "required": True},
    'password': {"type": "string", "empty": False, "required": True},
    'fullname': {"type": "string", "empty": False, "required": True},
    'cnpjCpf': {"type": "string", "empty": False, "required": False},
    'phone': {"type": "string", "empty": False, "required": False},
    'areaCode': {"type": "string", "empty": False, "required": False},
    'company': {"type": "string", "empty": False, "required": True},
    'companyType': {"type": "string", "empty": False, "required": True},
    'activity': {"type": "string", "empty": False, "required": True},
    'addressId': {"type": "integer", "empty": False, "required": False},
    'address': {"type": "dict", "empty": True, "required": False}
}


def validate(data, schema):
    v = Validator(schema)

    if not v.validate(data):
        return v.errors, False

    return data, True
