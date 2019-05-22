import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK

from parkings.tests.api.utils import check_required_fields

list_url = reverse("enforcement:v1:check_parking")


@pytest.fixture
def parking_data():
    return {
        "registration_number": "ABC-123",
        "location": {"longitude": 24.924441, "latitude": 60.182013},
    }


def test_check_parking_required_fields(staff_api_client):
    expected_required_fields = {"registration_number", "location"}
    check_required_fields(staff_api_client, list_url, expected_required_fields)


# TODO: Tests waiting for area/zone data ->
#
# def test_check_parking_valid_parking(operator, staff_api_client, parking_factory, parking_data):
#     parking = parking_factory(
#         registration_number="ABC-123",
#         operator=operator,
#     )
#
#     response = staff_api_client.post(list_url, data=parking_data)
#
#     assert response.status_code == HTTP_200_OK
#     assert response.data["status"] == "valid"
#     assert response.data["end_time"] == parking.time_end
#
#
# def test_check_parking_invalid_parking(
#     operator, staff_api_client, history_parking_factory, parking_data
# ):
#     history_parking_factory(
#         registration_number="ABC-123",
#         operator=operator,
#     )
#
#     response = staff_api_client.post(list_url, data=parking_data)
#
#     assert response.status_code == HTTP_200_OK
#     assert response.data["status"] == "invalid"
#
#
# def test_check_parking_valid_permit(staff_api_client, active_permit_factory):
#     permit = active_permit_factory()
#     reg_num = permit.subjects[0]["registration_number"]
#
#     valid_parking_data = {
#         "registration_number": reg_num,
#         "location": {"longitude": 24.924441, "latitude": 60.182013},
#     }
#
#     response = staff_api_client.post(list_url, data=valid_parking_data)
#
#     assert response.status_code == HTTP_200_OK
#     assert response.data["status"] == "valid"
#
#
# def test_check_parking_invalid_permit():
#     pass
