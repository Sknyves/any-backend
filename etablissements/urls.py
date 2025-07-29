from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EtablissementViewSet

router = DefaultRouter()
router.register(r'', EtablissementViewSet, basename='etablissements')

urlpatterns = router.urls