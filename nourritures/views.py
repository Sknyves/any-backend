from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from nourritures.models import Nourriture
from nourritures.serializers import NourritureSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .permissions import IsProprietaireNourriture
from django.core.exceptions import ValidationError

class NourritureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProprietaireNourriture]
    queryset = Nourriture.objects.all()
    serializer_class = NourritureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['IdEtablissement']

    # Action personnalisée pour la notation
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def rate(self, request, pk=None):
        nourriture = self.get_object()
        rating = request.data.get('rating')

        if not rating:
            return Response(
                {'error': 'Le champ "rating" est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rating = float(rating)
            if not (1 <= rating <= 5):
                raise ValidationError('La note doit être entre 1 et 5')
            
            nourriture.update_rating(rating)
            
            return Response({
                'success': True,
                'id': nourriture.id,
                'nom': nourriture.Nom,
                'new_rating': float(nourriture.Note),
                'review_count': nourriture.nb_avis
            })
        
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Une erreur est survenue'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )