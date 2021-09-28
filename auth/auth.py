from os import environ as env
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from dotenv import load_dotenv, find_dotenv
from urllib.request import urlopen
import constants
import json

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
ALGORITHMS = env.get(constants.ALGORITHMS)
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_LOGOUT_CALLBACK_URL = env.get(constants.AUTH0_LOGOUT_CALLBACK_URL)

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

    def to_json(self):
        return {
            'error': True,
            'status': self.status_code,
            'details': self.error
        }

# region Get token
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.',
            'error': 'Unauthorized'
        }, 401)

    auth_parts = auth.split()
    if auth_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".',
            'error': 'Unauthorized'
        }, 401)
    elif len(auth_parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.',
            'error': 'Unauthorized'
        }, 401)
    elif len(auth_parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.',
            'error': 'Unauthorized'
        }, 401)

    token = auth_parts[1]
    return token
    # endregion

# region Validate token
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.',
            'error': 'Unauthorized'
        }, 401)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.',
            'error': 'Unauthorized'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.',
                'error': 'Unauthorized'
            }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.',
                'error': 'Unauthorized'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.',
                'error': 'Bad request'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.',
                'error': 'Bad request'
            }, 400)
# endregion

# region Check permissions
def check_permissions(permission, payload):
    if permission == '':
        return True
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to check permissions.',
            'error': 'Bad request'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'no_permission',
            'description': 'User has no permission to access the requested content.',
            'error': 'Forbidden'
        }, 403)
    return True
# endregion

# region Requires Auth Decorator
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
# endregion

# region Get token
def get_token_auth_header_if_existent():
    auth = request.headers.get('Authorization', None)

    if not auth:
        return None

    auth_parts = auth.split()
    if auth_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".',
            'error': 'Unauthorized'
        }, 401)
    elif len(auth_parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.',
            'error': 'Unauthorized'
        }, 401)
    elif len(auth_parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.',
            'error': 'Unauthorized'
        }, 401)

    token = auth_parts[1]
    return token
    # endregion

# region Validate token
def verify_decode_jwt_if_existent(token):
    if not token:
        return None

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except:
        return None

    rsa_key = {}
    if 'kid' not in unverified_header:
        return None


    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except:
            return None
# endregion



# region Requires Auth Decorator
def gets_auth_if_existent(permission=''):
    def gets_auth_if_existent_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header_if_existent()
            payload = verify_decode_jwt_if_existent(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return gets_auth_if_existent_decorator
# endregion