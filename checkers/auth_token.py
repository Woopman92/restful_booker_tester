import re

from requests import Response


def check_successful_token_create_response(response: Response):
    assert re.fullmatch(r'[0-9a-f]{15}', response['token'])
