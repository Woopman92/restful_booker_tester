from http import HTTPStatus

from client.client import get_booking, get_booking_with_error_response, get_booking_ids


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
        assert set(item) == {"bookingid"}
        assert isinstance(item["bookingid"], int)
        
def check_get_booking_response(response: dict, expected_data: dict):
    assert response == expected_data

def check_create_booking_response(response: dict, expected_data: dict):
    assert isinstance(response['bookingid'], int)
    assert response['booking'] == expected_data

def check_update_booking_response(response: dict, expected_data: dict):
    assert response == expected_data

def check_booking_update(booking_id: int, expected_data: dict):
    response = get_booking(booking_id=booking_id)
    check_get_booking_response(response, expected_data)

def check_booking_deleted(booking_id: int):
    response = get_booking_with_error_response(
        expected_status_code=HTTPStatus.NOT_FOUND, booking_id=booking_id
    )
    assert response.text == 'Not Found'

def check_bookings_exist(booking_ids: list):
    response = get_booking_ids()
    for booking_id in booking_ids:
        assert {'bookingid': booking_id} in response