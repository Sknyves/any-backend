from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import NourritureViewSet

router = DefaultRouter()
router.register(r'', NourritureViewSet, basename='nourritures')

additional_urls = [
    path(
        '<int:pk>/rate/',
        NourritureViewSet.as_view({'post': 'rate'}),
        name='nourriture-rate'
    ),
]

urlpatterns = router.urls + additional_urls