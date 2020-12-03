"""
Validator
"""

from cerberus import Validator


INSERT_USER_SCHEMA = {
    'email': {"type": "string", "empty": False, "required": True},
    'password': {"type": "string", "empty": False, "required": True},
    'fullname': {"type": "string", "empty": False, "required": True},
    'cnpjCpf': {"type": "string", "empty": True, "required": False},
    'phone': {"type": "string", "empty": True, "required": False},
    'areaCode': {"type": "string", "empty": True, "required": False},
    'company': {"type": "string", "empty": False, "required": True},
    'companyType': {"type": "string", "empty": False, "required": True},
    'activity': {"type": "string", "empty": False, "required": True},
    'addressId': {"type": "integer", "empty": False, "required": False},
    'address': {
        "type": "dict", "empty": True, "required": False,
        'schema': {
            'cep': {'type': 'string', "empty": True, "required": False},
            'street': {'type': 'string', "empty": True, "required": False},
            'number': {'type': 'string', "empty": True, "required": False},
            'complement': {'type': 'string', "empty": True, "required": False},
            'city': {'type': 'string', "empty": True, "required": False},
            'state': {'type': 'string', "empty": True, "required": False},
            'country': {'type': 'string', "empty": True, "required": False},
        }
    }
}


def validate(data, schema):
    v = Validator(schema)

    if not v.validate(data):
        return v.errors, False

    return data, True
