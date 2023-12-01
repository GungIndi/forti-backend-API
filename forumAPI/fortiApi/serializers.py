from rest_framework import serializers
from .models import User, Post, Replies, Employee


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__' 