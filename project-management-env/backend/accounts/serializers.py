from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils import timezone


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        if validated_data.get('user_role'): 
            instance.user_role = validated_data.get('user_role', instance.user_role)
            instance.save()
            return instance
        else:
            raise serializers.ValidationError({'detail':"attr 'user_role' not declared."})

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'user_role', 'is_active')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    def validate_password(self, password):
        if password != self.initial_data.get('confirm_password'):
            raise serializers.ValidationError({"detail": "Passwords doesn't match"})
        validate_password(password, self.instance)
        return password
        
    def email_to_lower(self, email):
        return email.strip().lower()

    def create(self, data):
        email = self.email_to_lower(data.get('email'))
        user = User.objects.create_user(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=email, 
            password=data.get('password')
        )

        return user


    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'user_role')
        extra_kwargs = {'password': {'write_only': True}}


# User Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        email = self.email_to_lower(data.get('email'))
        password = data.get('password')
        user = authenticate(username=email, password=password)

        if user:
            if user.is_active:
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                return user

        message = {'detail': 'The email or password is incorrect'}
        raise serializers.ValidationError(message)

    def email_to_lower(self, email):
        return email.strip().lower()