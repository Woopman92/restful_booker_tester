from http import HTTPStatus

from checkers.booking import check_get_booking_response
from client.client import get_booking, get_booking_with_error_response


class TestCreateBookingPositive:

    def test_get_created_booking(self, user_booking):
        booking_data, booking_id = user_booking

        response = get_booking(booking_id=booking_id)

        check_get_booking_response(response, booking_data)

    def test_get_nonexistent_booking(self, user_booking):
        booking_data, booking_id = user_booking

        response = get_booking_with_error_response(
            expected_status_code=HTTPStatus.NOT_FOUND, booking_id=booking_id + 10000
        )
        assert response.text == 'Not Found'
