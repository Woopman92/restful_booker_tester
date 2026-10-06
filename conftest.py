import pytest

pytest.register_assert_rewrite('checkers', 'tests')
pytest_plugins = ['fixtures.booking', 'fixtures.auth_token', 'fixtures.booking_headers']
