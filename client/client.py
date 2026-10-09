import logging
import time
from datetime import date
from http import HTTPStatus

import pytest
import requests

logger = logging.getLogger(__name__)

HOST = 'https://restful-booker.herokuapp.com'
CREATE_TOKEN_URL = HOST + '/auth'
GET_BOOKING_IDS_URL = HOST + '/booking'
GET_BOOKING = GET_BOOKING_IDS_URL + '/{booking_id}'
CREATE_BOOKING_URL = GET_BOOKING_IDS_URL
UPDATE_BOOKING_URL = GET_BOOKING
PARTIAL_UPDATE_BOOKING_URL = UPDATE_BOOKING_URL
DELETE_BOOKING = GET_BOOKING
HEALTH_CHECK = HOST + '/ping'


def create_token(expected_status_code=HTTPStatus.OK, data: dict = None, headers: dict = None):
    return make_request(
        method='POST', url=CREATE_TOKEN_URL, expected_status_code=expected_status_code, data=data, headers=headers
    ).json()


def get_booking_ids(
    expected_status_code=HTTPStatus.OK,
    firstname: str | None = None,
    lastname: str | None = None,
    checkin: date | None = None,
    checkout: date | None = None,
):
    """
    Send request GET /booking
    :param expected_status_code: Expected response HTTP status code
    :param firstname: Return bookings with a specific firstname
    :param lastname: Return bookings with a specific lastname
    :param checkin: Return bookings that have a checkin date greater than or equal to the set checkin date.
    Format must be CCYY-MM-DD
    :param checkout: Return bookings that have a checkout date greater than or equal to the set checkout date.
    Format must be CCYY-MM-DD
    """
    params = {
        'firstname': firstname,
        'lastname': lastname,
        'checkin': checkin,
        'checkout': checkout,
    }
    params = {key: value for key, value in params.items() if value is not None}
    return make_request(
        method='GET', url=GET_BOOKING_IDS_URL, expected_status_code=expected_status_code, params=params
    ).json()


def create_booking(expected_status_code=HTTPStatus.OK, payload: dict = None, headers: dict = None, **kwargs):
    return make_request(
        method='POST',
        url=CREATE_BOOKING_URL,
        expected_status_code=expected_status_code,
        json=payload,
        headers=headers,
        **kwargs
    ).json()


def create_booking_xml(expected_status_code=HTTPStatus.OK, payload: dict = None, headers: dict = None, **kwargs):
    headers = headers or {'Content-Type': 'text/xml', 'Accept': 'application/xml'}

    return make_request(
        method='POST',
        url=CREATE_BOOKING_URL,
        expected_status_code=expected_status_code,
        data=payload,
        headers=headers,
        **kwargs
    )


def create_booking_with_error_response(
    expected_status_code=HTTPStatus.BAD_REQUEST, payload: dict = None, headers: dict = None, **kwargs
):
    return make_request(
        method='POST',
        url=CREATE_BOOKING_URL,
        expected_status_code=expected_status_code,
        json=payload,
        headers=headers,
        **kwargs
    )


def get_booking(expected_status_code=HTTPStatus.OK, booking_id: int = None):
    return make_request(
        method='GET', url=GET_BOOKING.format(booking_id=booking_id), expected_status_code=expected_status_code
    ).json()


def get_booking_xml(expected_status_code=HTTPStatus.OK, booking_id: int = None):
    headers = {'Accept': 'application/xml'}
    return make_request(
        method='GET',
        url=GET_BOOKING.format(booking_id=booking_id),
        expected_status_code=expected_status_code,
        headers=headers
    ).text


def get_booking_with_error_response(
    expected_status_code=HTTPStatus.BAD_REQUEST, booking_id: int = None, headers: dict = None
):
    return make_request(
        method='GET',
        url=GET_BOOKING.format(booking_id=booking_id),
        expected_status_code=expected_status_code,
        headers=headers
    )


def update_booking(
    expected_status_code=HTTPStatus.OK, booking_id: int = None, payload: dict = None, headers: dict = None, **kwargs
):
    return make_request(
        method='PUT',
        url=UPDATE_BOOKING_URL.format(booking_id=booking_id),
        expected_status_code=expected_status_code,
        json=payload,
        headers=headers,
        **kwargs
    ).json()


def update_booking_xml(
    expected_status_code=HTTPStatus.OK, booking_id: int = None, payload: str = None, headers: dict = None, **kwargs
):
    headers = headers or {'Content-Type': 'text/xml', 'Accept': 'application/xml'}

    return make_request(
        method='PUT',
        url=UPDATE_BOOKING_URL.format(booking_id=booking_id),
        expected_status_code=expected_status_code,
        data=payload,
        headers=headers,
        **kwargs
    )


def update_booking_with_error_response(
    expected_status_code=HTTPStatus.BAD_REQUEST,
    booking_id: int = None,
    payload: dict = None,
    headers: dict = None,
    **kwargs
):
    return make_request(
        method='PUT',
        url=UPDATE_BOOKING_URL.format(booking_id=booking_id),
        expected_status_code=expected_status_code,
        json=payload,
        headers=headers,
        **kwargs
    )


def partial_update_booking(
    expected_status_code=HTTPStatus.OK, booking_id: int = None, payload: dict = None, headers: dict = None, **kwargs
):
    return make_request(
        method='PATCH',
        url=PARTIAL_UPDATE_BOOKING_URL.format(booking_id=booking_id),
        expected_status_code=expected_status_code,
        json=payload,
        headers=headers,
        **kwargs
    ).json()


def partial_update_booking_xml(
    expected_status_code=HTTPStatus.OK, booking_id: int = None, payload: dict = None, headers: dict = None, **kwargs
):
    return make_request(
        method='PATCH',
        url=PARTIAL_UPDATE_BOOKING_URL.format(booking_id=booking_id),
        expected_status_code=expected_status_code,
        data=payload,
        headers=headers,
        **kwargs
    )


def partial_update_booking_with_error_response(
    expected_status_code=HTTPStatus.BAD_REQUEST,
    booking_id: int = None,
    payload: dict = None,
    headers: dict = None,
    **kwargs
):
    return make_request(
        method='PATCH',
        url=PARTIAL_UPDATE_BOOKING_URL.format(booking_id=booking_id),
        expected_status_code=expected_status_code,
        json=payload,
        headers=headers,
        **kwargs
    )


def delete_booking(expected_status_code=HTTPStatus.CREATED, booking_id: int = None, headers: dict = None, **kwargs):
    return make_request(
        method='DELETE',
        url=DELETE_BOOKING.format(booking_id=booking_id),
        expected_status_code=expected_status_code,
        headers=headers,
        **kwargs
    )


def delete_booking_with_error_response(
    expected_status_code=HTTPStatus.BAD_REQUEST, booking_id: int = None, headers: dict = None, **kwargs
):
    return make_request(
        method='DELETE',
        url=DELETE_BOOKING.format(booking_id=booking_id),
        expected_status_code=expected_status_code,
        headers=headers,
        **kwargs
    )


def wait_for_host(
    wait_time: int = 100,
    retry_count: int = 10,
    available_timeout: int = 5,
    required_successful_connections: int = 1,
) -> None:

    successful_connections_count = 0

    for _ in range(retry_count):
        time.sleep(wait_time / retry_count)

        if successful_connections_count == required_successful_connections:
            logger.info('The service is operating successfully')
            break

        try:
            logger.info('Waiting a response from the host')
            response = requests.get(url=HEALTH_CHECK, timeout=available_timeout)
            response.raise_for_status()
            successful_connections_count += 1
        except requests.exceptions.RequestException:
            successful_connections_count = 0

    else:
        logger.exception('Did not receive a response from the host')
        pytest.exit('Did not receive a response from the host')


def make_request(
    method: str,
    url: str,
    expected_status_code=HTTPStatus.OK,
    headers: dict = None,
    data: dict = None,
    json: dict = None,
    params: dict = None,
    **kwargs
):
    response = requests.request(method=method, url=url, headers=headers, data=data, json=json, params=params, **kwargs)
    assert response.status_code == expected_status_code, \
        f'The status code {response.status_code} does not match the expected one {expected_status_code}'
    return response
