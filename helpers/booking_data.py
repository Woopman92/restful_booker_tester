from datetime import date
from datetime import timedelta

from helpers.common import generate_unique_string


def get_create_booking_data(
    firstname: str | None = None,
    lastname: str | None = None,
    totalprice: int = 100,
    depositpaid: bool = True,
    checkin: str | None = None,
    checkout: str | None = None,
    additionalneeds: str | None = None,
):
    """
    Prepare POST /booking request payload
    :param firstname: Firstname for the guest who made the booking
    :param lastname: Lastname for the guest who made the booking
    :param totalprice: The total price for the booking
    :param depositpaid: Whether the deposit has been paid or not
    :param checkin: Date the guest is checking in. Format YYYY-MM-DD
    :param checkout: Date the guest is checking out. Format YYYY-MM-DD
    :param additionalneeds: Any other needs the guest has
    """
    firstname = firstname or generate_unique_string()
    lastname = lastname or generate_unique_string()
    today_date = date.today()
    checkin = checkin or str(today_date)
    checkout = checkout or str(today_date + timedelta(days=5))
    additionalneeds = additionalneeds or generate_unique_string(length=25)
    response = {
        'firstname': firstname,
        'lastname': lastname,
        'totalprice': totalprice,
        'depositpaid': depositpaid,
        'bookingdates': {'checkin': checkin, 'checkout': checkout},
        'additionalneeds': additionalneeds
    }
    return response


def get_updated_booking_data(
    existing_booking_data: dict,
    firstname: str | None = None,
    lastname: str | None = None,
    totalprice: int | None = None,
    depositpaid: bool = True,
    checkin: str | None = None,
    checkout: str | None = None,
    additionalneeds: str | None = None,
):
    """
    Prepare PUT /booking/:id request payload
    :param firstname: Firstname for the guest who made the booking
    :param lastname: Lastname for the guest who made the booking
    :param totalprice: The total price for the booking
    :param depositpaid: Whether the deposit has been paid or not
    :param checkin: Date the guest is checking in. Format YYYY-MM-DD
    :param checkout: Date the guest is checking out. Format YYYY-MM-DD
    :param additionalneeds: Any other needs the guest has
    :param existing_booking_data: Existing booking data
    """
    firstname = firstname or generate_unique_string()
    lastname = lastname or generate_unique_string()
    if (old_totalprice := existing_booking_data.get('totalprice')) and not totalprice:
        totalprice = old_totalprice + 1
    totalprice = totalprice or 100
    today_date = date.today()
    if (old_checkin := existing_booking_data.get('bookingdates').get('checkin')) and not checkin:
        checkin = str(date.fromisoformat(old_checkin) + timedelta(days=1))
    if (old_checkout := existing_booking_data.get('bookingdates').get('checkout')) and not checkout:
        checkout = str(date.fromisoformat(old_checkout) + timedelta(days=1))
    checkin = checkin or str(today_date)
    checkout = checkout or str(today_date + timedelta(days=5))
    additionalneeds = additionalneeds or generate_unique_string(length=25)
    response = {
        'firstname': firstname,
        'lastname': lastname,
        'totalprice': totalprice,
        'depositpaid': depositpaid,
        'bookingdates': {'checkin': checkin, 'checkout': checkout},
        'additionalneeds': additionalneeds
    }
    return response
