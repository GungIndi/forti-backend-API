from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password  
from django.db import IntegrityError
from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *


def main(request):
    return HttpResponse('<h1> Hello </h1>')

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'message': 'Unique constraint violated. User with this value already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        is_valid_password = check_password(password, user.password)

        if is_valid_password:
            # Authentication successful
            # token, created = Token.objects.create(user=user)
            return Response({'username': username, 'token': username+user.password}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    filterset_fields = ['identity_number', 'username', 'user_role']
    @action(detail=False, methods=['GET'])
    def get(self, request, *args, **kwargs):
        filters = {}
        for field in self.filterset_fields:
            param = self.request.query_params.get(field, None)
            if param:
                filters[field] = param

        if filters:
            users = User.objects.filter(**filters)
            if users.exists():
                serializer = self.get_serializer(users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No Matching Data Found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return super().get(request, *args, **kwargs)

class GetUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'])
    def search_by_id(self, request, id):
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'No Matching Data Found'}, status=status.HTTP_404_NOT_FOUND)
            
    @action(detail=False, methods=['PUT'])
    def update_user(self, request, id):
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['DELETE'])
    def delete_user(self, request, id):
        try:
            user = User.objects.get(pk=id)
            user.delete()
            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'message': 'No Matching Data Found'}, status=status.HTTP_404_NOT_FOUND)



class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    
    filterset_fields = ['category', 'content']

    @action(detail=False, methods=['GET'])
    def get(self, request, *args, **kwargs):
        filters = {}
        for field in self.filterset_fields:
            param = self.request.query_params.get(field, None)
            if param:
                lookup = 'icontains' if field == 'content' else 'exact'
                filters[field + '__' + lookup] = param

        if filters:
            posts = Post.objects.filter(**filters)
        else:
            posts = self.queryset.all()

        sort_by = self.request.query_params.get('sort', None)
        order_by = self.request.query_params.get('order', 'asc')
        allowed_fields = ['id', 'category', 'content', 'created_at', 'updated_at', 'likes', 'dislikes']

        if sort_by:
            if sort_by == 'likes':
                annotate_field = 'total_likes'
                feedback_type = 'like'
            elif sort_by == 'dislikes':
                annotate_field = 'total_dislikes'
                feedback_type = 'dislike'
            elif sort_by in allowed_fields:
                annotate_field = sort_by
                feedback_type = None
            else:
                # Handle invalid sort_by parameter
                return Response({'message': 'Invalid Sort Parameter'}, status=status.HTTP_400_BAD_REQUEST)

            # Annotate the queryset with total_likes or total_dislikes
            if feedback_type:
                posts = posts.annotate(**{annotate_field: Count('feedback', filter=Q(feedback__feedback_type=feedback_type))})
            else:
                posts = posts.annotate(**{annotate_field: Count('feedback')})

            # Order the queryset based on the annotated field
            if order_by == 'desc':
                annotate_field = '-' + annotate_field
            posts = posts.order_by(annotate_field)
        elif sort_by in allowed_fields:
            if order_by == 'desc':
                sort_by = '-' + sort_by
            posts = posts.order_by(sort_by)

        if posts.exists():
            limit = self.request.query_params.get('limit', None)
            if limit and limit.isdigit():
                limit = int(limit)
                posts = posts[:limit]

            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If no matching data is found, return an appropriate response
            return Response({'message': 'No Matching Data Found'}, status=status.HTTP_404_NOT_FOUND)

class GetPost(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=False, methods=['GET'])
    def search_by_id(self, request, id):
        try:
            post = Post.objects.get(pk=id)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'message': 'No Matching Data Found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['PUT'])
    def update_post(self, request, id):
        try:
            post = Post.objects.get(pk=id)
            serializer = UserSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'message': 'No Matching Data Found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['DELETE'])
    def delete_post(self, request, id):
        try:
            post = Post.objects.get(pk=id)
            post.delete()
            return Response({'message':'Query Successful'}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response({'message': 'No Matching Data Found'}, status=status.HTTP_404_NOT_FOUND)

class RepliesView(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    serializer_class = RepliesSerializer

class GetReply(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = RepliesSerializer

    @action(detail=False, methods=['GET'])
    def search_by_id(self, request, id):
        try:
            reply = Reply.objects.get(pk=id)
            serializer = RepliesSerializer(reply)
            return Response( serializer.data, status=status.HTTP_200_OK)
        except Reply.DoesNotExist:
            return Response({'message': 'No Matching Data Found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['PUT'])
    def update_reply(self, request, id):
        try:
            reply = Reply.objects.get(pk=id)
            serializer = RepliesSerializer(reply, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Reply.DoesNotExist:
            return Response({'message': 'No Matching Data Found'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['DELETE'])
    def delete_reply(self, request, id):
        try:
            reply = Reply.objects.get(pk=id)
            reply.delete()
            return Response({'message':'Query Successful'}, status=status.HTTP_204_NO_CONTENT)
        except Reply.DoesNotExist:
            return Response({'message': 'No Matching Data Found'}, status=status.HTTP_404_NOT_FOUND)

class RepliesFeedbackView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = RepliesFeedback.objects.all()
    serializer_class = RepliesFeedbackSerializer

class PostFeedbackView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = PostFeedback.objects.all()
    serializer_class = PostFeedbackSerializer