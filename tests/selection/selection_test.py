import pytest
from rest_framework import status

from tests.factories import JobFactory


@pytest.mark.django_db
def test_selection_create(client, user_access_token):
    user, access_token = user_access_token
    job_list = JobFactory.create_batch(10)

    data = {
        "name": "Название подборки",
        "items": [job.pk for job in job_list]
    }

    expected_data = {
        "id": 1,
        "owner": user.username,
        "name": "Название подборки",
        "items": [job.pk for job in job_list]
    }

    response = client.post("/selection/", data=data, HTTP_AUTHORIZATION=f"Bearer {access_token}")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_data
