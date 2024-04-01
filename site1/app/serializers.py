
from django.contrib.auth.models import Group
from .models import Customer
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = [ 'id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['url', 'name']