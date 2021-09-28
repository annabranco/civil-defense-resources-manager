ALGORITHMS = 'ALGORITHMS'
AUTH0_AUDIENCE = 'AUTH0_AUDIENCE'
AUTH0_CALLBACK_URL = 'AUTH0_CALLBACK_URL'
AUTH0_CLIENT_ID = 'AUTH0_CLIENT_ID'
AUTH0_CLIENT_SECRET = 'AUTH0_CLIENT_SECRET'
AUTH0_DOMAIN = 'AUTH0_DOMAIN'
AUTH0_LOGOUT_CALLBACK_URL = 'AUTH0_LOGOUT_CALLBACK_URL'
DATABASE_URL = 'DATABASE_URL'
DB_HOST = 'DB_HOST'
DB_NAME = 'DB_NAME'
DB_PWD = 'DB_PWD'
DB_TEST_NAME = 'DB_TEST_NAME'
DB_USER = 'DB_USER'

HTTP_RESPONSES = {
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method not Allowed',
    422: 'Unprocessable Entity',
    500: 'Server Error',
}

AUTH_ERROR_MESSAGES = {
    'probably_expired': 'There was a problem with your authentication. Probably your token has expired or it is no longer valid. Please, login again and try to repeat the request.',
    'authorization_header_missing': 'Authorization header is expected.',
    'no_bearer': 'Authorization header must start with "Bearer".',
    'token_not_found': 'Token not found.',
    'no_bearer_token': 'Authorization header must be bearer token.',
    'auth_malformed': 'Authorization malformed.',
    'token_expired': 'Token expired.',
    'invalid_claims': 'Incorrect claims. Please, check the audience and issuer.',
    'parsing_failed': 'Unable to parse authentication token.',
    'key_not_found': 'Unable to find the appropriate key.',
    'permissions_failed': 'Unable to check permissions.',
    'no_permission': 'User has no permission to access the requested content.'
}

ERROR_MESSAGES = {
    'vol_not_found': 'There are no volunteers with the provided id.',
    'gr_not_found': 'There are no groups with the provided id.',
    'rol_not_found': 'There are no roles with the provided id.',
    'veh_not_found': 'There are no vehicles with the provided id.',
    'ser_not_found': 'There are no services with the provided id.',
    'body_needed': 'A data object should be sent on the request.',
    'missing_data': 'There are missing required data on the object sent.',
    'invalid_role': 'The role id provided in not valid.',
    'invalid_group': 'The group id provided in not valid.',
    'max_groups': 'A volunteer cannot be on more than 5 groups.',
    'invalid_list': 'There is at least one invalid id on the lists provided.',
    'no_change': 'No information was changed on the request.',
    'wrong_type': 'An attribute sent has a wrong type. Please double check all values.',
    'bad_date': 'The date provided is incorrectly formated. Please use [YYYY-MM-DD].',
    'bad_full_date': 'The date provided is incorrectly formated. Please use [YYYY-MM-DD, hh:mm].',
    'forbidden_del': 'Sorry, this resource is permanent and cannot be deleted.',
    'forbidden_upd': 'Sorry, this resource is permanent and cannot be changed.',
    'forbidden_date_upd': 'This service has already passed and can no longer be changed.',
    'forbidden_not_own': 'Sorry, you are not authorized to access this data.',
    'not_found': 'Resource not found on database.',
    'not_allowed': 'Are you handling the correct endpoint?',
    'bad_request': 'Your request is incorrect and cannot be processed. Please double check it.',
    'unprocessable': 'Your request could not be processed. Are you sure your request is correct?',
    'server_error': 'That\'s very embarassing, but something has failed on the backend... :('
}

