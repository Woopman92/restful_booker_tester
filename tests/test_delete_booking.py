from http import HTTPStatus

import pytest
from pytest_lazy_fixtures import lf

from checkers.booking import check_booking_deleted
from checkers.booking import check_bookings_exist
from client.client import delete_booking
from client.client import delete_booking_with_error_response


class TestDeleteBookingPositive:

    @pytest.mark.parametrize(
        'headers', [lf('update_booking_headers_with_cookie'), lf('update_booking_headers_with_auth')]
    )
    def test_delete_booking(self, user_bookings_with_diff_checkin, headers):
        _, three_created_booking_ids = user_bookings_with_diff_checkin
        booking_for_del_id = three_created_booking_ids[0]

        response = delete_booking(booking_id=booking_for_del_id, headers=headers)

        assert response.text == 'Created'
        check_booking_deleted(booking_id=booking_for_del_id)
        # check that the other bookings created have not been deleted
        check_bookings_exist(booking_ids=list(three_created_booking_ids)[1:])


class TestDeleteBookingNegative:

    def test_delete_nonexistent_booking(self, nonexistent_booking_id, update_booking_headers_with_cookie):
        response = delete_booking_with_error_response(
            expected_status_code=HTTPStatus.METHOD_NOT_ALLOWED,
            booking_id=nonexistent_booking_id,
            headers=update_booking_headers_with_cookie
        )

        assert response.text == 'Method Not Allowed'

    @pytest.mark.parametrize(
        'header', [
            {'Cookie': 'token=123'},
            {'Authorization': 'Basic 123'},
        ],
        ids=['invalid_cookie_header', 'invalid_auth_header']
    )
    def test_delete_booking_with_invalid_auth_headers(self, user_booking, header):
        _, booking_id = user_booking
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        headers.update(header)

        response = delete_booking_with_error_response(
            expected_status_code=HTTPStatus.FORBIDDEN,
            booking_id=booking_id,
            headers=headers,
        )

        assert response.text == 'Forbidden'
        # checking that the booking details have not changed
        check_bookings_exist(booking_ids=[booking_id])
