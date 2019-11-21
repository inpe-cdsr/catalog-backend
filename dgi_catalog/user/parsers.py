"""
Validator
"""

from cerberus import Validator

ADDRESS_SCHEMA = {
    'cep': {"type": "string", "empty": False, "required": True},
    'street': {"type": "string", "empty": False, "required": True},
    'number': {"type": "string", "empty": False, "required": True},
    'city': {"type": "string", "empty": False, "required": True},
    'state': {"type": "string", "empty": False, "required": True},
    'country': {"type": "string", "empty": False, "required": True},
}

INSERT_USER_SCHEMA = {
    'email': {"type": "string", "empty": False, "required": True},
    'password': {"type": "string", "empty": False, "required": True},
    'fullname': {"type": "string", "empty": False, "required": True},
    'cnpjCpf': {"type": "string", "empty": False, "required": False},
    'phone': {"type": "string", "empty": False, "required": True},
    'areaCode': {"type": "string", "empty": False, "required": True},
    'company': {"type": "string", "empty": False, "required": True},
    'companyType': {"type": "string", "empty": True, "required": True},
    'activity': {"type": "string", "empty": True, "required": True},
    'address': { 
        "type": "dict",
        "schema": ADDRESS_SCHEMA
    }
}


def validate(data, schema):
    v = Validator(schema)

    if not v.validate(data):
        return v.errors, False

    return data, True
