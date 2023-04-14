import pytest
from rest_framework import status

from ads.serializers import JobDetailSerializer
from tests.factories import JobFactory


@pytest.mark.django_db
def test_ad_detail(client, access_token):
    job = JobFactory.create()
    response = client.get(f"/ad/{job.pk}/")
    assert response.status_code == 401

    response = client.get(f"/ad/{job.pk}/", HTTP_AUTHORIZATION=f"Bearer {access_token}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == JobDetailSerializer(job).data
