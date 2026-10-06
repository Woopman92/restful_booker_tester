from datetime import date
from datetime import timedelta

import pytest

from client.client import create_booking
from client.client import get_booking_ids
from helpers.booking_data import get_create_booking_data
from helpers.common import generate_unique_string


@pytest.fixture
def user_booking():
    data = get_create_booking_data()
    booking = create_booking(payload=data)
    return data, booking['bookingid']


@pytest.fixture
def user_bookings_with_diff_firstnames():
    """
    Create 3 bookings with 2 of which having the same firstname
    """
    firstname = generate_unique_string(length=10)
    booking_data_1 = get_create_booking_data(firstname=firstname)
    booking_data_2 = get_create_booking_data()
    booking_data_3 = get_create_booking_data(firstname=firstname)
    booking_1 = create_booking(payload=booking_data_1)
    booking_3 = create_booking(payload=booking_data_3)
    create_booking(payload=booking_data_2)

    return firstname, (booking_1['bookingid'], booking_3['bookingid'])


@pytest.fixture
def user_bookings_with_diff_lastname():
    """
    Create 3 bookings with 2 of which having the same lastname
    """
    lastname = generate_unique_string(length=11)
    booking_data_1 = get_create_booking_data(lastname=lastname)
    booking_data_2 = get_create_booking_data(lastname=lastname)
    booking_data_3 = get_create_booking_data()
    booking_1 = create_booking(payload=booking_data_1)
    booking_2 = create_booking(payload=booking_data_2)
    create_booking(payload=booking_data_3)

    return lastname, (booking_1['bookingid'], booking_2['bookingid'])


@pytest.fixture
def user_bookings_with_diff_checkin():
    """
    Create 3 bookings with different checkin params:
    1 – equal to the set checkin date
    2 – lesser
    3 – bigger
    """
    checkin = date.today() + timedelta(days=1)
    booking_data_1 = get_create_booking_data(checkin=str(checkin))
    booking_data_2 = get_create_booking_data(checkin=str(checkin + timedelta(days=1)))
    booking_data_3 = get_create_booking_data(checkin=str(checkin + timedelta(days=-1)))
    booking_1 = create_booking(payload=booking_data_1)
    booking_2 = create_booking(payload=booking_data_2)
    booking_3 = create_booking(payload=booking_data_3)

    return checkin, (booking_1['bookingid'], booking_2['bookingid'], booking_3['bookingid'])


@pytest.fixture
def user_bookings_with_diff_checkout():
    """
    Create 3 bookings with different checkout params:
    1 – equal to the set checkout date
    2 – lesser
    3 – bigger
    """
    checkin = date.today()
    checkout = checkin + timedelta(days=5)
    booking_data_1 = get_create_booking_data(checkin=str(checkin), checkout=str(checkout))
    booking_data_2 = get_create_booking_data(checkin=str(checkin), checkout=str(checkout + timedelta(days=1)))
    booking_data_3 = get_create_booking_data(checkin=str(checkin), checkout=str(checkout + timedelta(days=-1)))
    booking_1 = create_booking(payload=booking_data_1)
    booking_2 = create_booking(payload=booking_data_2)
    booking_3 = create_booking(payload=booking_data_3)

    return checkout, (booking_1['bookingid'], booking_2['bookingid'], booking_3['bookingid'])


@pytest.fixture
def user_bookings_with_diff_params():
    """
    Create 5 bookings with different checkout params:
    1 – equal to the set params
    2 – with different firstname param
    3 – with different lastname param
    4 - with different checkin param
    5 - with different checkout param
    """
    firstname = generate_unique_string()
    lastname = generate_unique_string()
    checkin = date.today()
    checkout = checkin + timedelta(days=5)
    booking_data_1 = get_create_booking_data(
        firstname=firstname, lastname=lastname, checkin=str(checkin), checkout=str(checkout)
    )
    firstname_2 = firstname + '2'
    booking_data_2 = get_create_booking_data(
        firstname=firstname_2, lastname=lastname, checkin=str(checkin), checkout=str(checkout)
    )
    lastname_3 = lastname + '3'
    booking_data_3 = get_create_booking_data(
        firstname=firstname, lastname=lastname_3, checkin=str(checkin), checkout=str(checkout)
    )
    checkin_4 = checkin + timedelta(days=-1)
    booking_data_4 = get_create_booking_data(
        firstname=firstname, lastname=lastname, checkin=str(checkin_4), checkout=str(checkout)
    )
    checkout_5 = checkout + timedelta(days=-1)
    booking_data_5 = get_create_booking_data(
        firstname=firstname, lastname=lastname, checkin=str(checkin), checkout=str(checkout_5)
    )
    booking_ids = []
    for data in (booking_data_1, booking_data_2, booking_data_3, booking_data_4, booking_data_5):
        booking = create_booking(payload=data)
        booking_ids.append(booking['bookingid'])

    return {'firstname': firstname, 'lastname': lastname, 'checkin': checkin, 'checkout': checkout}, booking_ids


@pytest.fixture
def nonexistent_booking_id():
    response = get_booking_ids()
    return max([j for i in response for j in i.values()]) + 10000
