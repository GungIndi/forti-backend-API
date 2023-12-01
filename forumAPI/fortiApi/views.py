from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .serializers import UserSerializer, EmployeeSerializer
from .models import User, Employee

def main(request):
    return HttpResponse('<h1> Hello </h1>')


class UserView(generics.CreateAPIView, generics.DestroyAPIView, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class EmployeeView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer