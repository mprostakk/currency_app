from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            password = validated_data.pop('password')
            email = validated_data.pop('email')
        except KeyError:
            raise ValidationError(detail='Error')

        user = User(username=email, email=email)
        user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            raise ValidationError(detail='User exists')

        return user
