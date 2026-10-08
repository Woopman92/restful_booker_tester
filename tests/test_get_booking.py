from http import HTTPStatus

import pytest

from checkers.booking import check_get_booking_response
from checkers.booking import check_get_booking_xml_response
from client.client import get_booking
from client.client import get_booking_with_error_response
from client.client import get_booking_xml


@pytest.mark.positive
class TestGetBookingPositive:

    def test_get_created_booking(self, user_booking):
        booking_data, booking_id = user_booking

        response = get_booking(booking_id=booking_id)

        check_get_booking_response(response, booking_data)

    def test_get_created_booking_xml(self, user_booking):
        booking_data, booking_id = user_booking

        response = get_booking_xml(booking_id=booking_id)

        check_get_booking_xml_response(response, booking_data)


@pytest.mark.negative
class TestGetBookingNegative:

    def test_get_nonexistent_booking(self, user_booking):
        booking_data, booking_id = user_booking

        response = get_booking_with_error_response(
            expected_status_code=HTTPStatus.NOT_FOUND, booking_id=booking_id + 10000
        )
        assert response.text == 'Not Found'

    def test_get_booking_with_invalid_accept_header(self, user_booking):
        headers = {'Accept': 'text/plain'}
        booking_data, booking_id = user_booking

        response = get_booking_with_error_response(
            expected_status_code=HTTPStatus.IM_A_TEAPOT, booking_id=booking_id, headers=headers
        )
        assert response.text == "I'm a Teapot"
