from copy import copy
from datetime import date
from http import HTTPStatus

import pytest
from dict2xml import dict2xml
from pytest_lazy_fixtures import lf

from checkers.booking import check_booking_updated
from checkers.booking import check_update_booking_response
from checkers.booking import check_update_booking_xml_response
from client.client import partial_update_booking
from client.client import partial_update_booking_with_error_response
from client.client import partial_update_booking_xml
from client.client import update_booking_with_error_response
from helpers.booking_data import get_updated_booking_data


@pytest.mark.positive
class TestPartialUpdateBookingPositive:

    @pytest.mark.parametrize(
        'headers', [lf('update_booking_headers_with_cookie'), lf('update_booking_headers_with_auth')]
    )
    def test_partial_update_booking(self, user_booking, headers):
        existing_booking_data, booking_id = user_booking
        data = get_updated_booking_data(existing_booking_data=existing_booking_data)

        response = partial_update_booking(booking_id=booking_id, payload=data, headers=headers)

        check_update_booking_response(response=response, expected_data=data)
        check_booking_updated(booking_id=booking_id, expected_data=data)

    @pytest.mark.parametrize(
        'update_booking_headers_with_cookie', [
            {'Content-Type': 'text/xml', 'Accept': 'application/xml'},
        ],
        indirect=True
    )
    def test_partial_update_booking_xml(self, user_booking, update_booking_headers_with_cookie):
        existing_booking_data, booking_id = user_booking
        data = get_updated_booking_data(existing_booking_data=existing_booking_data)
        data_xml = dict2xml(data, wrap='booking')

        response = partial_update_booking_xml(
            booking_id=booking_id, payload=data_xml, headers=update_booking_headers_with_cookie
        )

        check_update_booking_xml_response(response=response, expected_data=data)
        check_booking_updated(booking_id=booking_id, expected_data=data)

    def test_partial_update_booking_with_same_params(self, user_booking, update_booking_headers_with_cookie):
        existing_booking_data, booking_id = user_booking

        response = partial_update_booking(
            booking_id=booking_id, payload=existing_booking_data, headers=update_booking_headers_with_cookie
        )

        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize(
        'value', ['A', 'Alexander', 'John Doe', 'John-Doe', 'O`Connor', 'A' * 1000, ''],
        ids=[
            'one char name',
            'common name',
            'name with space',
            'name with hyphen',
            'name with backtick',
            'long name',
            'empty string',
        ]
    )
    @pytest.mark.parametrize('param', ['firstname', 'lastname'])
    def test_partial_update_booking_with_diff_valid_names(
        self, user_booking, update_booking_headers_with_cookie, param, value
    ):
        existing_booking_data, booking_id = user_booking
        data = {param: value}

        response = partial_update_booking(
            booking_id=booking_id, payload=data, headers=update_booking_headers_with_cookie
        )

        existing_booking_data[param] = value
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize('value', [0, 1, 999999999, -1, 2.5, 2.6, 3.5, '100'])
    def test_partial_update_booking_with_diff_valid_total_price_values(
        self, user_booking, update_booking_headers_with_cookie, value
    ):
        existing_booking_data, booking_id = user_booking
        data = {'totalprice': value}

        response = partial_update_booking(
            booking_id=booking_id, payload=data, headers=update_booking_headers_with_cookie
        )

        existing_booking_data['totalprice'] = int(value)
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize('value', [True, False, 1, 0, '', 'false'])
    def test_partial_update_booking_with_diff_valid_depositpaid_values(
        self, user_booking, update_booking_headers_with_cookie, value
    ):
        existing_booking_data, booking_id = user_booking
        data = {'depositpaid': value}

        response = partial_update_booking(
            booking_id=booking_id, payload=data, headers=update_booking_headers_with_cookie
        )

        existing_booking_data['depositpaid'] = bool(value)
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize('value', ['2026/01/01', '01-01-2026', '2026-1-1', '2026-01-01'])
    def test_partial_update_booking_with_diff_bookingdates_date_formats(
        self, user_booking, update_booking_headers_with_cookie, value
    ):
        existing_booking_data, booking_id = user_booking
        data = {'bookingdates': {'checkin': value, 'checkout': value}}

        response = partial_update_booking(
            booking_id=booking_id, payload=data, headers=update_booking_headers_with_cookie
        )

        existing_booking_data['bookingdates']['checkin'] = '2026-01-01'
        existing_booking_data['bookingdates']['checkout'] = '2026-01-01'
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize(
        'value', ['Breakfast, dinner and supper', 'Breakfast', '', 123, 'A' * 1000],
        ids=['string with spaces', 'one word string', 'empty string', 'int', 'long string']
    )
    def test_partial_update_booking_with_diff_valid_additionalneeds(
        self, user_booking, update_booking_headers_with_cookie, value
    ):
        existing_booking_data, booking_id = user_booking
        data = {'additionalneeds': value}

        response = partial_update_booking(
            booking_id=booking_id, payload=data, headers=update_booking_headers_with_cookie
        )

        existing_booking_data['additionalneeds'] = value
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    def test_partial_update_booking_with_empty_payload(self, user_booking, update_booking_headers_with_cookie):
        existing_booking_data, booking_id = user_booking

        response = partial_update_booking(
            booking_id=booking_id,
            payload={},
            headers=update_booking_headers_with_cookie,
        )

        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)


@pytest.mark.negative
class TestPartialUpdateBookingNegative:

    def test_partial_update_nonexistent_booking(self, nonexistent_booking_id, update_booking_headers_with_cookie):
        data = {'firstname': 'Bobek'}

        response = partial_update_booking_with_error_response(
            expected_status_code=HTTPStatus.METHOD_NOT_ALLOWED,
            booking_id=nonexistent_booking_id,
            payload=data,
            headers=update_booking_headers_with_cookie,
        )

        assert response.text == 'Method Not Allowed'

    @pytest.mark.parametrize(
        'booking_data',
        [
            {'firstname': 123},
            {'lastname': 123},
        ],
    )
    def test_partial_update_booking_with_invalid_type_param(
        self, user_booking, update_booking_headers_with_cookie, booking_data
    ):
        existing_booking_data, booking_id = user_booking

        response = partial_update_booking(
            booking_id=booking_id,
            payload=booking_data,
            headers=update_booking_headers_with_cookie,
        )

        # Need to clarify the expected result. This is a test of the function's current behavior
        existing_booking_data.update(booking_data)
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize(
        'booking_data', [
            {'firstname': None},
            {'lastname': None},
            {'totalprice': None},
            {'additionalneeds': None},
        ],
        ids=['firstname', 'lastname', 'totalprice', 'additionalneeds']
    )
    def test_partial_update_booking_with_non_type_param(
        self, user_booking, update_booking_headers_with_cookie, booking_data
    ):
        existing_booking_data, booking_id = user_booking

        response = partial_update_booking(
            booking_id=booking_id,
            payload=booking_data,
            headers=update_booking_headers_with_cookie,
        )

        # Need to clarify the expected result. This is a test of the function's current behavior
        existing_booking_data.update(booking_data)
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    def test_partial_update_booking_with_non_type_depositpaid_param(
        self, user_booking, update_booking_headers_with_cookie
    ):
        existing_booking_data, booking_id = user_booking

        response = partial_update_booking(
            booking_id=booking_id,
            payload={'depositpaid': None},
            headers=update_booking_headers_with_cookie,
        )

        # Need to clarify the expected result. This is a test of the function's current behavior
        existing_booking_data['depositpaid'] = bool(None)
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize('param', ['checkin', 'checkout'])
    def test_partial_update_booking_with_non_type_bookingdates_param(
        self, user_booking, update_booking_headers_with_cookie, param
    ):
        existing_booking_data, booking_id = user_booking
        updated_bookingdates = copy(existing_booking_data['bookingdates'])
        updated_bookingdates[param] = None
        data = {'bookingdates': updated_bookingdates}

        response = partial_update_booking(
            booking_id=booking_id,
            payload=data,
            headers=update_booking_headers_with_cookie,
        )

        # Need to clarify the expected result. This is a test of the function's current behavior
        existing_booking_data['bookingdates'][param] = str(date.fromtimestamp(0))
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize('value', ['2018-01-01', None], ids=['string', 'nontype'])
    def test_partial_update_booking_with_invalid_type_bookingdates(
        self, user_booking, update_booking_headers_with_cookie, value
    ):
        existing_booking_data, booking_id = user_booking
        data = {'bookingdates': value}

        response = update_booking_with_error_response(
            expected_status_code=HTTPStatus.BAD_REQUEST,
            booking_id=booking_id,
            payload=data,
            headers=update_booking_headers_with_cookie,
        )

        assert response.text == 'Bad Request'
        # checking that the booking details have not changed
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize('param', ['checkin', 'checkout'])
    def test_partial_update_booking_without_bookingdates_required_params(
        self, user_booking, update_booking_headers_with_cookie, param
    ):
        existing_booking_data, booking_id = user_booking
        updated_bookingdates = copy(existing_booking_data['bookingdates'])
        updated_bookingdates.pop(param)
        data = {'bookingdates': updated_bookingdates}

        response = partial_update_booking(
            booking_id=booking_id,
            payload=data,
            headers=update_booking_headers_with_cookie,
        )

        # Need to clarify the expected result. This is a test of the function's current behavior
        existing_booking_data['bookingdates'][param] = '0NaN-aN-aN'
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize('value', ['2018-13-01', '2018-01-32'], ids=['invalid_month', 'invalid_day'])
    @pytest.mark.parametrize('param', ['checkin', 'checkout'])
    def test_partial_update_booking_with_invalid_bookingdates(
        self, user_booking, update_booking_headers_with_cookie, param, value
    ):
        existing_booking_data, booking_id = user_booking
        updated_bookingdates = copy(existing_booking_data['bookingdates'])
        updated_bookingdates[param] = value
        data = {'bookingdates': updated_bookingdates}

        response = partial_update_booking(
            booking_id=booking_id, payload=data, headers=update_booking_headers_with_cookie
        )

        # Need to clarify the expected result. This is a test of the function's current behavior
        existing_booking_data['bookingdates'][param] = '0NaN-aN-aN'
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize('param', ['checkin', 'checkout'])
    def test_partial_update_booking_with_invalid_non_leap_year_bookingdates(
        self, user_booking, update_booking_headers_with_cookie, param
    ):
        existing_booking_data, booking_id = user_booking
        updated_bookingdates = copy(existing_booking_data['bookingdates'])
        updated_bookingdates[param] = '2026-02-29'
        data = {'bookingdates': updated_bookingdates}

        response = partial_update_booking(
            booking_id=booking_id, payload=data, headers=update_booking_headers_with_cookie
        )

        # Need to clarify the expected result. This is a test of the function's current behavior
        existing_booking_data['bookingdates'][param] = '2026-03-01'
        check_update_booking_response(response=response, expected_data=existing_booking_data)
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize('header', [
        {'Cookie': 'token=123'},
        {'Authorization': 'Basic 123'},
    ])
    def test_partial_update_booking_with_invalid_auth_headers(self, user_booking, header):
        existing_booking_data, booking_id = user_booking
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        headers.update(header)
        data = get_updated_booking_data(existing_booking_data=existing_booking_data)

        response = partial_update_booking_with_error_response(
            expected_status_code=HTTPStatus.FORBIDDEN,
            booking_id=booking_id,
            payload=data,
            headers=headers,
        )

        assert response.text == 'Forbidden'
        # checking that the booking details have not changed
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize(
        'update_booking_headers_with_cookie', [
            {'Content-Type': 'text/plain'},
        ], indirect=True
    )
    def test_partial_update_booking_with_invalid_content_type_header(
        self, user_booking, update_booking_headers_with_cookie
    ):
        existing_booking_data, booking_id = user_booking
        data = get_updated_booking_data(existing_booking_data=existing_booking_data)

        response = partial_update_booking(
            booking_id=booking_id, payload=data, headers=update_booking_headers_with_cookie
        )

        check_update_booking_response(response=response, expected_data=existing_booking_data)
        # checking that the booking details have not changed
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)

    @pytest.mark.parametrize(
        'update_booking_headers_with_cookie', [
            {'Accept': 'text/plain'},
        ], indirect=True
    )
    def test_partial_update_booking_with_invalid_accept_header(self, user_booking, update_booking_headers_with_cookie):
        existing_booking_data, booking_id = user_booking
        data = get_updated_booking_data(existing_booking_data=existing_booking_data)

        response = partial_update_booking_with_error_response(
            expected_status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            booking_id=booking_id,
            payload=data,
            headers=update_booking_headers_with_cookie,
        )

        assert response.text == 'Internal Server Error'
        check_booking_updated(booking_id=booking_id, expected_data=data)

    def test_update_booking_with_malformed_json(self, user_booking, update_booking_headers_with_cookie):
        existing_booking_data, booking_id = user_booking
        data = get_updated_booking_data(existing_booking_data=existing_booking_data)
        malformed_data = str(data)[:-1]

        response = update_booking_with_error_response(
            expected_status_code=HTTPStatus.BAD_REQUEST,
            booking_id=booking_id,
            data=malformed_data,
            headers=update_booking_headers_with_cookie,
        )

        assert response.text == 'Bad Request'
        # checking that the booking details have not changed
        check_booking_updated(booking_id=booking_id, expected_data=existing_booking_data)
