import uuid
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import datetime
from datetime import timedelta

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

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_or_email = attrs.get("username")
        password = attrs.get("password")

        # get the user by username or email
        from django.contrib.auth import get_user_model
        User = get_user_model()

        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid username/email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid username/email or password")
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        access_exp = datetime.fromtimestamp(access_token['exp'])

        # SimpleJWT generate token
        data = super().validate({"username": user.username, "password": password})
        return {
            "access": str(access_token),
            "refresh": str(refresh),
            "user": {
                #"id": user.id,
                "name": user.username,
                "email": user.email,
                #"role": "admin" if user.is_staff else "user",  # You can customize this
            },
            "session": {
                "expires_at": access_exp.isoformat()
            }
        }
