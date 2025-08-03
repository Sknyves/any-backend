from rest_framework import serializers
from utilisateurs.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'telephone', 'role', 'is_active', 'photo_de_profil']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'photo_de_profil': {'required': False}
        }

    def get_photo_de_profil(self, obj):
        if obj.photo_de_profil:
            return self.context['request'].build_absolute_uri(obj.photo_de_profil.url)
        return None

    def create(self, validated_data):
        # Extraction du mot de passe avant la création
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hachage correct du mot de passe
        user.is_active = True
        user.save()
        return user