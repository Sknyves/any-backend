from rest_framework import viewsets
from nourritures.models import Nourriture
from nourritures.serializers import NourritureSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import IsProprietaireNourriture

class NourritureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProprietaireNourriture]
    queryset = Nourriture.objects.all()
    serializer_class = NourritureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['IdEtablissement']
    