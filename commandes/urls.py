from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CommandeViewSet

router = DefaultRouter()
router.register(r'', CommandeViewSet, basename='commandes')

urlpatterns = router.urls