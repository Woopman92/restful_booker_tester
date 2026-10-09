import pytest

from client.client import create_token
from constants import CREATE_TOKEN_CREDS


@pytest.fixture
def user_token():
    response = create_token(data=CREATE_TOKEN_CREDS)
    return response['token']
