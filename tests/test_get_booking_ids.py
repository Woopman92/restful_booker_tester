from checkers.booking import check_get_booking_ids_response_structure
from client.client import get_booking_ids
from helpers.common import generate_unique_string


class TestGetBookingIdsPositive:

    def test_get_all_booking_ids(self):
        response = get_booking_ids()

        check_get_booking_ids_response_structure(response)

    def test_get_added_booking_id(self, user_booking):
        _, booking_id = user_booking

        response = get_booking_ids()

        assert {'bookingid': booking_id} in response

    def test_get_booking_ids_filtered_by_firstname(self, user_bookings_with_diff_firstnames):
        firstname, booking_ids = user_bookings_with_diff_firstnames
        response = get_booking_ids(firstname=firstname)

        assert response == [{'bookingid': booking_ids[0]}, {'bookingid': booking_ids[1]}]

    def test_get_booking_ids_filtered_by_lastname(self, user_bookings_with_diff_lastname):
        lastname, booking_ids = user_bookings_with_diff_lastname
        response = get_booking_ids(lastname=lastname)

        assert response == [{'bookingid': booking_ids[0]}, {'bookingid': booking_ids[1]}]

    def test_get_booking_ids_filtered_by_checkin(self, user_bookings_with_diff_checkin):
        checkin, booking_ids = user_bookings_with_diff_checkin
        response = get_booking_ids(checkin=checkin)

        assert {'bookingid': booking_ids[1]} in response
        assert {'bookingid': booking_ids[2]} not in response
        # The query does not return the booking_id
        # for which the checkin value matches the one specified in the parameter
        assert {'bookingid': booking_ids[0]} in response

    def test_get_booking_ids_filtered_by_checkout(self, user_bookings_with_diff_checkout):
        checkout, booking_ids = user_bookings_with_diff_checkout
        response = get_booking_ids(checkout=checkout)

        assert {'bookingid': booking_ids[0]} in response
        # The query doesn't return the booking_id
        # that has checkout date greater than the one specified in the parameter
        assert {'bookingid': booking_ids[1]} in response
        # The query return the booking_id
        # that has checkout date lesser than the one specified in the parameter
        assert {'bookingid': booking_ids[2]} not in response

    def test_get_booking_ids_by_all_params(self, user_bookings_with_diff_params):
        request_params, booking_ids = user_bookings_with_diff_params
        response = get_booking_ids(**request_params)

        # The query does not return the booking_id
        # for which the checkin value matches the one specified in the parameter
        assert {'bookingid': booking_ids[0]} in response
        assert {'bookingid': booking_ids[1]} not in response
        assert {'bookingid': booking_ids[2]} not in response
        assert {'bookingid': booking_ids[3]} not in response
        assert {'bookingid': booking_ids[4]} not in response

    def test_get_booking_ids_empty_response(self):
        firstname = generate_unique_string()

        response = get_booking_ids(firstname=firstname)

        assert response == []
