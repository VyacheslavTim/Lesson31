import pytest
from rest_framework import status

from ads.serializers import JobListSerializer
from tests.factories import JobFactory


@pytest.mark.django_db
def test_ad_list(client):
    job_list = JobFactory.create_batch(4)

    response = client.get(f"/ad/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "count": 4,
        "next": None,
        "previous": None,
        "results": JobListSerializer(job_list, many=True).data
        }
