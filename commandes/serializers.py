from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from commandes.models import Commande

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'
        read_only_fields = ('IdUser', 'Statut')
    
    def validate(self, data):
        if not self.context['request'].user.is_authenticated:
            raise PermissionDenied("Vous devez être connecté")
        return data