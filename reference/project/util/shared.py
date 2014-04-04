
import exceptions

TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
STATS_NAME = 'name'
STATS_VALUE = 'value'
JSON_CONTENT = 'application/json'

NAME = 'name'
SYNOPSIS = 'synopsis'
VERSION = 'version'
INSTITUTION = 'institution'
RELEASE_TIME = 'release_time'
RELASE_TIME_JSON = 'releaseTime'
SUPPORT_EMAIL = 'support_email'
SUPPORT_EMAIL_JSON = 'supportEmail'
CATEGORY = 'category'
RESEARCH_SUBJECT = 'research_subject'
RESEARCH_SUBJECT_JSON = 'researchSubject'
TAGS = 'tags'

FIELD_NOT_SET_ERROR = 'Field {0} not set'


def validate_info_json(expected, data):
    """ Validate that all the required fields in the input are present.

    """
    if expected <= set(data):
        return True
    raise ValueError('Invalid content')

def get_field(data, field_name):
    """ Get a field from the json data and return it. If it is not thair raise
        an error

    """
    if field_name in data and data.get(field_name):
        return data.get(field_name)

    raise ValueError(FIELD_NOT_SET_ERROR.format(field_name))


def num (s):
    """ Parse a number from a string.

    """
    try:
        return int(s)
    except exceptions.ValueError:
        return float(s)
