from rest_framework import serializers
from nourritures.models import Nourriture

class NourritureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nourriture
        fields = '__all__'