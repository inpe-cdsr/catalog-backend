"""
common.py
"""

from werkzeug.exceptions import BadRequest, InternalServerError

from jwt import encode as __jwt_encode__, decode as __jwt_decode__, DecodeError, InvalidAlgorithmError

from dgi_catalog.environment import JWT_SECRET, JWT_ALGORITHM


# JWT

def jwt_encode(json_dict):
    return __jwt_encode__(json_dict, JWT_SECRET, algorithm=JWT_ALGORITHM).decode("utf-8")


def jwt_decode(token):
    try:
        return __jwt_decode__(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except DecodeError as error:
        raise BadRequest('Error when decoding token. (error: ' + str(error) + ')')
    except InvalidAlgorithmError as error:
        raise BadRequest('Invalid algorithm. (error: ' + str(error) + ')')
