from rest_framework.permissions import BasePermission
from etablissements.models import Etablissement

class IsProprietaireNourriture(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.IdEtablissement.IdUser == request.user