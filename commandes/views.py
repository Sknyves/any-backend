from rest_framework import viewsets
from commandes.models import Commande
from commandes.serializers import CommandeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

class CommandeViewSet(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['IdUser', 'Statut']
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(IdUser=self.request.user)