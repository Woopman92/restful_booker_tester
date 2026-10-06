import json
from datetime import date
from datetime import timedelta
from http import HTTPStatus

import pytest

from checkers.booking import check_create_booking_response
from client.client import create_booking
from client.client import create_booking_with_error_response
from helpers.booking_data import get_create_booking_data


class TestCreateBookingPositive:

    def test_create_booking(self):
        data = get_create_booking_data()

        response = create_booking(payload=data)

        check_create_booking_response(response=response, expected_data=data)

    @pytest.mark.parametrize('value', ['A', 'Alexander', 'John Doe', 'John-Doe', 'O`Connor', 'A' * 1000, ''])
    @pytest.mark.parametrize('param', ['firstname', 'lastname'])
    def test_create_booking_with_diff_valid_names(self, param, value):
        data = get_create_booking_data()
        data[param] = value

        response = create_booking(payload=data)

        check_create_booking_response(response=response, expected_data=data)

    @pytest.mark.parametrize('value', [0, 1, 999999999, -1, 2.5, 2.6, 3.5, '100'])
    def test_create_booking_with_diff_valid_total_price_values(self, value):
        data = get_create_booking_data(totalprice=value)

        response = create_booking(payload=data)

        data['totalprice'] = int(value)
        check_create_booking_response(response=response, expected_data=data)

    @pytest.mark.parametrize('value', [True, False, 1, 0, '', 'false'])
    def test_create_booking_with_diff_valid_depositpaid_values(self, value):
        data = get_create_booking_data(depositpaid=value)

        response = create_booking(payload=data)

        data['depositpaid'] = bool(value)
        check_create_booking_response(response=response, expected_data=data)

    @pytest.mark.parametrize('value', ['2026/01/01', '01-01-2026', '2026-1-1'])
    @pytest.mark.parametrize('param', ['checkin', 'checkout'])
    def test_create_booking_with_diff_format_checkin_checkout_values(self, param, value):
        data = get_create_booking_data()
        data['bookingdates'][param] = value

        response = create_booking(payload=data)

        data['bookingdates'][param] = '2026-01-01'
        check_create_booking_response(response=response, expected_data=data)

    def test_create_booking_with_checkin_greater_than_checkout(self):
        checkin = date.today()
        checkout = checkin + timedelta(days=-1)
        data = get_create_booking_data(checkin=str(checkin), checkout=str(checkout))

        response = create_booking(payload=data)

        check_create_booking_response(response=response, expected_data=data)

    @pytest.mark.parametrize('value', ['Breakfast, dinner and supper', 'Breakfast', '', 123, 'A' * 1000])
    def test_create_booking_with_diff_valid_additionalneeds(self, value):
        data = get_create_booking_data(additionalneeds=value)

        response = create_booking(payload=data)

        check_create_booking_response(response=response, expected_data=data)

    def test_create_booking_without_additionalneeds_param(self):
        data = get_create_booking_data()
        data.pop('additionalneeds')

        response = create_booking(payload=data)

        check_create_booking_response(response=response, expected_data=data)

    # Need to clarify the expected result. This is a test of the function's current behavior
    def test_recreate_booking_with_same_params(self, user_booking):
        data, booking_id = user_booking

        response = create_booking(payload=data)

        assert response['bookingid'] != booking_id
        check_create_booking_response(response=response, expected_data=data)


class TestCreateBookingNegative:

    @pytest.mark.parametrize('param', [
        'firstname',
        'lastname',
        'totalprice',
        'depositpaid',
        'bookingdates',
    ])
    def test_create_booking_without_required_param(self, param):
        data = get_create_booking_data()
        data.pop(param)

        response = create_booking_with_error_response(
            expected_status_code=HTTPStatus.INTERNAL_SERVER_ERROR, payload=data
        )

        assert response.text == 'Internal Server Error'

    @pytest.mark.parametrize('param', ['checkin', 'checkout'])
    def test_create_booking_without_bookingdates_required_params(self, param):
        data = get_create_booking_data()
        data['bookingdates'].pop(param)

        response = create_booking_with_error_response(
            expected_status_code=HTTPStatus.INTERNAL_SERVER_ERROR, payload=data
        )

        assert response.text == 'Internal Server Error'

    @pytest.mark.parametrize(
        'param,value',
        [
            ('firstname', 123),
            ('lastname', 123),
            ('bookingdates', '2018-01-01'),
        ],
    )
    def test_create_booking_with_invalid_type_param(self, param, value):
        data = get_create_booking_data()
        data[param] = value

        response = create_booking_with_error_response(
            expected_status_code=HTTPStatus.INTERNAL_SERVER_ERROR, payload=data
        )

        assert response.text == 'Internal Server Error'

    @pytest.mark.parametrize('value', ['2018-13-01', '2018-01-32'], ids=['invalid_month', 'invalid_day'])
    @pytest.mark.parametrize('param', ['checkin', 'checkout'])
    def test_create_booking_with_invalid_bookingdates(self, param, value):
        data = get_create_booking_data()
        data['bookingdates'][param] = value

        response = create_booking(payload=data)

        # Need to clarify the expected result. This is a test of the function's current behavior
        data['bookingdates'][param] = '0NaN-aN-aN'
        check_create_booking_response(response=response, expected_data=data)

    @pytest.mark.parametrize('param', ['checkin', 'checkout'])
    def test_create_booking_with_invalid_non_leap_year_bookingdates(self, param):
        data = get_create_booking_data()
        data['bookingdates'][param] = '2026-02-29'

        response = create_booking(payload=data)

        # Need to clarify the expected result. This is a test of the function's current behavior
        data['bookingdates'][param] = '2026-03-01'
        check_create_booking_response(response=response, expected_data=data)

    @pytest.mark.parametrize(
        'data',
        [
            {'firstname': None},
            {'lastname': None},
            {'totalprice': None},
            {'depositpaid': None},
            {'bookingdates': None},
            {'bookingdates': {'checkin': None, 'checkout': '2018-01-01'}},
            {'bookingdates': {'checkin': '2018-01-01', 'checkout': None}},
            {'bookingdates': {'checkin': None, 'checkout': None}},
        ],
    )
    def test_create_booking_with_non_type_param(self, data):
        booking_data = get_create_booking_data()
        booking_data.update(data)

        response = create_booking_with_error_response(
            expected_status_code=HTTPStatus.INTERNAL_SERVER_ERROR, payload=data
        )

        assert response.text == 'Internal Server Error'

    def test_create_booking_with_invalid_content_type_header(self):
        data = get_create_booking_data()
        headers = {'Content-Type': 'text/plain'}

        response = create_booking_with_error_response(
            expected_status_code=HTTPStatus.INTERNAL_SERVER_ERROR, data=json.dumps(data), headers=headers
        )

        assert response.text == 'Internal Server Error'

    def test_create_booking_with_invalid_accept_header(self):
        data = get_create_booking_data()
        headers = {'Accept': 'text/plain'}

        response = create_booking_with_error_response(
            expected_status_code=HTTPStatus.INTERNAL_SERVER_ERROR, data=json.dumps(data), headers=headers
        )

        assert response.text == 'Internal Server Error'

    def test_create_booking_with_malformed_json(self):
        data = get_create_booking_data()
        malformed_data = str(data)[:-1]
        headers = {'Content-Type': 'application/json'}

        response = create_booking_with_error_response(
            expected_status_code=HTTPStatus.BAD_REQUEST, data=malformed_data, headers=headers
        )

        assert response.text == 'Bad Request'
