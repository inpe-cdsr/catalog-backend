"""
Validator
"""

from cerberus import Validator


INSERT_USER_SCHEMA = {
    'email': {"type": "string", "empty": False, "required": True},
    'password': {"type": "string", "empty": False, "required": True},
    'fullname': {"type": "string", "empty": False, "required": True},
    'cnpjCpf': {"type": "string", "empty": False, "required": True},
    'phone': {"type": "string", "empty": False, "required": False},
    'areaCode': {"type": "string", "empty": False, "required": False},
    'company': {"type": "string", "empty": False, "required": False},
    'companyType': {"type": "string", "empty": True, "required": False},
    'activity': {"type": "string", "empty": False, "required": False},
    # 'userType': {"type": "string", "empty": True, "required": True},
    'addressId': {"type": "integer", "empty": False, "required": True}
}


def validate(data, schema):
    v = Validator(schema)

    if not v.validate(data):
        return v.errors, False

    return data, True
