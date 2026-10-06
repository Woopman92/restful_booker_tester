import pytest

from constants import AUTH_HEADER_VALUE


@pytest.fixture(params=[{}])
def update_booking_headers_with_cookie(request, user_token):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': f'token={user_token}',
    }
    headers.update(**request.param)

    return headers


@pytest.fixture(params=[{}])
def update_booking_headers_with_auth(request, user_token):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': AUTH_HEADER_VALUE,
    }
    headers.update(**request.param)

    return headers