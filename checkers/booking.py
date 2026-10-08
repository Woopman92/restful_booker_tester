import xml.etree.ElementTree as ET
from http import HTTPStatus

from client.client import get_booking
from client.client import get_booking_ids
from client.client import get_booking_with_error_response


def check_get_booking_ids_response_structure(data: list[dict]):
    """
    Checks that the data matches the structure:
    [
        {
            "bookingid": 1
        },
        {
            "bookingid": 2
        },
        {
            "bookingid": 3
        }
    ]
    """
    assert isinstance(data, list)

    for item in data:
        assert isinstance(item, dict)
        assert set(item) == {'bookingid'}
        assert isinstance(item['bookingid'], int)


def check_get_booking_response(response: dict, expected_data: dict):
    assert response == expected_data


def check_get_booking_xml_response(response: str, expected_data: dict):
    root = ET.fromstringlist(response)

    assert root.find('firstname').text == expected_data['firstname']
    assert root.find('lastname').text == expected_data['lastname']
    assert root.find('totalprice').text == str(expected_data['totalprice'])
    assert root.find('depositpaid').text == str(expected_data['depositpaid']).lower()

    booking_dates = root.find('bookingdates')

    assert booking_dates.find('checkin').text == expected_data['bookingdates']['checkin']
    assert booking_dates.find('checkout').text == expected_data['bookingdates']['checkout']

    assert root.find('additionalneeds').text == expected_data['additionalneeds']


def check_create_booking_response(response: dict, expected_data: dict):
    assert isinstance(response['bookingid'], int)
    assert response['booking'] == expected_data


def check_create_booking_xml_response(response: str, expected_data: dict):
    root = ET.fromstringlist(response)

    assert int(root.find('bookingid').text)

    booking = root.find('booking')

    assert booking.find('firstname').text == expected_data['firstname']
    assert booking.find('lastname').text == expected_data['lastname']
    assert booking.find('totalprice').text == str(expected_data['totalprice'])
    assert booking.find('depositpaid').text == str(expected_data['depositpaid']).lower()

    booking_dates = booking.find('bookingdates')

    assert booking_dates.find('checkin').text == expected_data['bookingdates']['checkin']
    assert booking_dates.find('checkout').text == expected_data['bookingdates']['checkout']

    assert booking.find('additionalneeds').text == expected_data['additionalneeds']


def check_update_booking_response(response: dict, expected_data: dict):
    assert response == expected_data


def check_update_booking_xml_response(response: str, expected_data: dict):
    root = ET.fromstringlist(response)

    assert root.find('firstname').text == expected_data['firstname']
    assert root.find('lastname').text == expected_data['lastname']
    assert root.find('totalprice').text == str(expected_data['totalprice'])
    assert root.find('depositpaid').text == str(expected_data['depositpaid']).lower()

    booking_dates = root.find('bookingdates')

    assert booking_dates.find('checkin').text == expected_data['bookingdates']['checkin']
    assert booking_dates.find('checkout').text == expected_data['bookingdates']['checkout']

    assert root.find('additionalneeds').text == expected_data['additionalneeds']


def check_booking_updated(booking_id: int, expected_data: dict):
    response = get_booking(booking_id=booking_id)
    check_get_booking_response(response, expected_data)


def check_booking_updated_xml(booking_id: int, expected_data: dict):
    response = get_booking(booking_id=booking_id)
    check_get_booking_xml_response(response, expected_data)


def check_booking_deleted(booking_id: int):
    response = get_booking_with_error_response(expected_status_code=HTTPStatus.NOT_FOUND, booking_id=booking_id)
    assert response.text == 'Not Found'


def check_bookings_exist(booking_ids: list):
    response = get_booking_ids()
    for booking_id in booking_ids:
        assert {'bookingid': booking_id} in response
