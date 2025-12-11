from rest_framework import serializers
from .models import AppUser


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = [
            'id', 'email', 'full_name', 'display_name',
            'money', 'profile_picture',
        ]
        read_only_fields = ['id', 'display_name', 'full_name']


class AppUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['full_name', 'profile_picture']
