from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Etablissement, HoraireOuverture
from .serializers import EtablissementSerializer, HoraireOuvertureSerializer
from .permissions import IsProprietaireOrReadOnly


class EtablissementViewSet(viewsets.ModelViewSet):
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer
    permission_classes = [IsProprietaireOrReadOnly]

    def get_serializer_context(self):
        """Ajoute la requête au contexte du serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(IdUser=self.request.user)

    @action(detail=True, methods=['get', 'post'])
    def horaires(self, request, pk=None):
        etablissement = self.get_object()

        if request.method == 'POST':
            serializer = HoraireOuvertureSerializer(
                data=request.data,
                context={'etablissement': etablissement}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(etablissement=etablissement)
            return Response(serializer.data, status=201)

        horaires = etablissement.horaires.all()
        serializer = HoraireOuvertureSerializer(horaires, many=True)
        return Response(serializer.data)