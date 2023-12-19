from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from .serializers import *
from .models import *


def main(request):
    return HttpResponse('<h1> Hello </h1>')


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GetUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['identity_number', 'user_name', 'user_role']

    @action(detail=False, methods=['GET'])
    def search_by_parameter(self, request):
        filters = {}
        for field in self.filterset_fields:
            param = request.query_params.get(field)
            if param:
                filters[field] = param

        if not filters:
            return Response({"error": "No filter parameters provided"}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(**filters)

        if users.exists():
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Users not found."}, status=status.HTTP_404_NOT_FOUND)

class UserDetailView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class ReplyView(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = RepliesSerializer

class PostFeedbackView(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = PostFeedbackSerializer

class RepliesFeedbackView(generics.CreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = RepliesFeedbackSerializer

    
class EmployeeView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer