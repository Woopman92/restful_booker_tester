import pytest
from pytest_lazy_fixtures import lf

from checkers.booking import check_booking_deleted, check_bookings_exist
from client.client import delete_booking


class TestDeleteBookingPositive:

    @pytest.mark.parametrize('headers', [lf('update_booking_headers_with_cookie'), lf('update_booking_headers_with_auth')])
    def test_delete_booking(self, user_bookings_with_diff_checkin, headers):
        _, three_created_booking_ids = user_bookings_with_diff_checkin
        booking_for_del_id = three_created_booking_ids[0]

        response = delete_booking(booking_id=booking_for_del_id, headers=headers)

        assert response.text == 'Created'
        check_booking_deleted(booking_id=booking_for_del_id)
        check_bookings_exist(booking_ids=list(three_created_booking_ids)[1:])

