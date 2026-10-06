import pytest

pytest.register_assert_rewrite('checkers', 'tests')
pytest_plugins = ['fixtures.booking', 'fixtures.token', 'fixtures.booking_headers']