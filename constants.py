AUTH0_DOMAIN = 'AUTH0_DOMAIN'
API_AUDIENCE = 'API_AUDIENCE'
ALGORITHMS = "ALGORITHMS"
DB_HOST = 'DB_HOST'
DB_USER = 'DB_USER'
DB_PWD = 'DB_PWD'
DB_NAME = 'DB_NAME'
DB_TEST_NAME = 'DB_TEST_NAME'
DATABASE_URL = 'DATABASE_URL'
HTTP_RESPONSES = {
    400: 'Bad Request',
    404: 'Not Found',
    405: 'Method not Allowed',
    422: 'Unprocessable Entity',
    500: 'Server Error',
}

ERROR_MESSAGES = {
    "vol_not_found": 'There are no volunteers with the provided id.',
    "gr_not_found": 'There are no groups with the provided id.',
    "rol_not_found": 'There are no roles with the provided id.',
    "veh_not_found": 'There are no vehicles with the provided id.',
    "body_needed": 'A data object should be sent on the request.',
    "missing_data": 'There are missing required data on the object sent.',
    "invalid_role": 'The role id provided in not valid.',
    "invalid_group": 'The group id provided in not valid.',
    "max_groups": 'A volunteer cannot be on more than 5 groups.',
    "invalid_list": 'There is at least one invalid id on the group list provided.',
    "no_change": 'No information was changed on the request.',
    "wrong_type": 'An attribute sent has a wrong type. Please double check all values.',
    "bad_date": 'A date provided is incorrectly formated. Please use YYYY-MM-DD.'
}