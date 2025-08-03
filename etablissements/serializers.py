from rest_framework import serializers
from etablissements.models import Etablissement, HoraireOuverture

class HoraireOuvertureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoraireOuverture
        fields = '__all__'
        read_only_fields = ('etablissement',)

class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = '__all__'
        extra_kwargs = {
            'IdUser': {'read_only': True},
            'Description': {'required': False, 'allow_blank': True},
            'Photo_de_couverture': {'required': False},
            'Horaire_ouverture': {'required': False, 'allow_blank': True}
        }

    def validate(self, data):
        errors = {}
        if not data.get('Nom'):
            errors['Nom'] = "Le nom est obligatoire"
        if not data.get('Emplacement'):
            errors['Emplacement'] = "L'emplacement est obligatoire"
        
        if errors:
            raise serializers.ValidationError(errors)
        return data