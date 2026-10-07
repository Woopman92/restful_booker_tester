import pytest

from client.client import wait_for_host
from config import WAIT_FOR_HOST

pytest.register_assert_rewrite('checkers', 'tests')
pytest_plugins = ['fixtures.booking', 'fixtures.auth_token', 'fixtures.booking_headers']


def pytest_sessionstart():
    if WAIT_FOR_HOST:
        wait_for_host()
