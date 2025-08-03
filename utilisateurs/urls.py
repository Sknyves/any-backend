from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CurrentUserView, UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='utilisateurs')

urlpatterns = [
    path('me/', CurrentUserView.as_view(), name='current-user'),
    *router.urls,
]