from .models import Profile

from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id',  'email', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
