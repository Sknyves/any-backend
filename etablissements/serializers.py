from rest_framework import serializers
from etablissements.models import Etablissement, HoraireOuverture

class HoraireOuvertureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoraireOuverture
        fields = '__all__'
        read_only_fields = ('etablissement',)

class EtablissementSerializer(serializers.ModelSerializer):
    horaires = HoraireOuvertureSerializer(many=True, read_only=True)
    
    class Meta:
        model = Etablissement
        fields = '__all__'