from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    email = serializers.EmailField()

    def validate_username(self,username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists')

    def validate_password(self,password):
        if len(password) < 8:
            raise ValidationError('Password must has at least 8 characters')
        return password

class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=6)

