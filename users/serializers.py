import uuid
from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password', 'email', 'is_anonymous']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Generate a unique username
        random_username = f"user_{uuid.uuid4().hex[:10]}"
        validated_data['username'] = random_username
        return User.objects.create_user(**validated_data)
