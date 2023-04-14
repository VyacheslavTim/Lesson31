# from django.urls import path
#
# from ads.views import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
#
# urlpatterns = [
#     path('', CategoryListView.as_view()),
#     path('<int:pk>/', CategoryDetailView.as_view()),
#     path('create/', CategoryCreateView.as_view()),
#     path('<int:pk>/update/', CategoryUpdateView.as_view()),
#     path('<int:pk>/delete/', CategoryDeleteView.as_view())
# ]
from rest_framework.routers import SimpleRouter

from ads.views import CatViewSet

cat_router = SimpleRouter()
cat_router.register("", CatViewSet)
urlpatterns = cat_router.urls
