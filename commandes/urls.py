from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommandeViewSet, stats_etablissement, commandes_etablissements_utilisateur

router = DefaultRouter()
router.register(r'', CommandeViewSet, basename='commandes')

urlpatterns = [
    path('', include(router.urls)),
    path('etablissement/<int:etablissement_id>/stats/', stats_etablissement, name='stats-etablissement'),
    path('owner/', commandes_etablissements_utilisateur, name='commandes-mes-etablissements'),
]