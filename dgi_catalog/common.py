"""
common.py
"""

from werkzeug.exceptions import BadRequest, InternalServerError

from jwt import encode as __jwt_encode__, decode as __jwt_decode__, DecodeError, InvalidAlgorithmError


# JWT

def jwt_encode(json_dict):
    return __jwt_encode__(json_dict, __JWT_SECRET__, algorithm=__JWT_ALGORITHM__).decode("utf-8")


def jwt_decode(token):
    try:
        return __jwt_decode__(token, __JWT_SECRET__, algorithms=[__JWT_ALGORITHM__])
    except DecodeError as error:
        raise BadRequest('Error when decoding token. (error: ' + str(error) + ')')
    except InvalidAlgorithmError as error:
        raise BadRequest('Invalid algorithm. (error: ' + str(error) + ')')
