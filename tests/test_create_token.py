import re
import pytest

from checkers.token import check_successful_token_create_response
from client.client import create_token
from constants import CREATE_TOKEN_CREDS


class TestCreateTokenPositive:

    def test_create_token(self):
        response = create_token(CREATE_TOKEN_CREDS)

        check_successful_token_create_response(response)

    def test_recreate_token(self, user_token):
        response = create_token(CREATE_TOKEN_CREDS)

        check_successful_token_create_response(response)
        assert response.json()['token'] != user_token


class TestCreateTokenNegative:

    @pytest.mark.parametrize(
        'data',
        [
            {'username': 'odmin', 'password': 'password123'},
            {'username': 'admin', 'password': 'password124'},
        ],
        ids=['wrong_username', 'wrong_password']
    )
    def test_create_token_with_wrong_credentials(self, data):
        response = create_token(data)

        assert response.json() == {'reason': 'Bad credentials'}
