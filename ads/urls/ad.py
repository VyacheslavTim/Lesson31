from django.urls import path
from rest_framework.routers import SimpleRouter

from ads.views import JobImageUpload, JobViewSet

router = SimpleRouter()
router.register("", JobViewSet)


urlpatterns = [
    path('<int:pk>/upload_image/', JobImageUpload.as_view())
]

urlpatterns += router.urls
