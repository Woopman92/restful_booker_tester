import pytest

from checkers.auth_token import check_successful_token_create_response
from client.client import create_token
from constants import CREATE_TOKEN_CREDS


@pytest.mark.positive
class TestCreateTokenPositive:

    def test_create_token(self):
        response = create_token(data=CREATE_TOKEN_CREDS)

        check_successful_token_create_response(response)

    def test_recreate_token(self, user_token):
        response = create_token(data=CREATE_TOKEN_CREDS)

        check_successful_token_create_response(response)
        assert response['token'] != user_token


@pytest.mark.negative
class TestCreateTokenNegative:

    @pytest.mark.parametrize(
        'data', [
            {'username': 'odmin', 'password': 'password123'},
            {'username': 'admin', 'password': 'password124'},
        ],
        ids=['wrong_username', 'wrong_password']
    )
    def test_create_token_with_wrong_credentials(self, data):
        response = create_token(data=data)

        assert response == {'reason': 'Bad credentials'}
