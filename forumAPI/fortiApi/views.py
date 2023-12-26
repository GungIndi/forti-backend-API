from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password  
from django.db import IntegrityError
from django.db.models import Count, Q, F
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from .serializers import *
from .models import *


def main(request):
    return HttpResponse('<h1> Hello </h1>')


class BaseAPIView(generics.GenericAPIView):
    def format_response(self, code, status, data):
        return Response({
            'code': code,
            'status': status,
            'data': data,
        }, status=code)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return BaseAPIView.format_response(self, status.HTTP_201_CREATED, "CREATED", serializer.data)
            return BaseAPIView.format_response(self,status.HTTP_400_BAD_REQUEST, "BAD_REQUEST", serializer._errors)
        except IntegrityError as e:
            return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST, "Unique constraint violated. User with this value already exists.", None)
    
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
            return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST, "User not found.", None)

        is_valid_password = check_password(password, user.password)

        if is_valid_password:
            return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", {'id': user.id,'username': username, 'token': username+user.password, 'user_role': user.user_role})
        else:
            # Authentication failed
            return BaseAPIView.format_response(self, status.HTTP_401_UNAUTHORIZED, "Invalid credentials.", None)
        
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return BaseAPIView.format_response(self, status.HTTP_200_OK, 'OK', serializer.data)

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
                return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
            else:
                return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
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
            return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
        except User.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
            
    @action(detail=False, methods=['PUT'])
    def update_user(self, request, id):
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
            else:
                return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST,  "BAD_REQUEST", serializer.errors)
        except User.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
        
    @action(detail=False, methods=['DELETE'])
    def delete_user(self, request, id):
        try:
            user = User.objects.get(pk=id)
            user.delete()
            return BaseAPIView.format_response(self, status.HTTP_204_NO_CONTENT, "User deleted successfully.", None)
        except User.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)

class PostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        else:
            return PostListSerializer
        
    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = PostListSerializer(posts, many=True)
        return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
    
    def post(self, request):
        try:
            serializer = PostCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return BaseAPIView.format_response(self, status.HTTP_201_CREATED, "CREATED", serializer.data)
            return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST,  "BAD_REQUEST", serializer.errors)
        except IntegrityError as e:
            return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST,  "BAD_REQUEST", serializer.errors)
    
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
            annotate_field = None  # Initialize annotation field
            feedback_type = None
            if sort_by == 'likes':
                annotate_field = 'total_likes'
                feedback_type = 'like'
            elif sort_by == 'dislikes':
                annotate_field = 'total_dislikes'
                feedback_type = 'dislike'
            elif sort_by in allowed_fields:
                if sort_by == 'id' or sort_by == 'created_at' or sort_by == 'updated_at':
                    posts = posts.order_by(F(sort_by).asc(nulls_last=True))
                else:
                    annotate_field = sort_by
                    feedback_type = None
            else:
                # Handle invalid sort_by parameter
                return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST,  "BAD_REQUEST", 'Invalid Parameter')

            # Annotate the queryset with total_likes or total_dislikes
            if feedback_type:
                posts = posts.annotate(**{annotate_field: Count('feedback', filter=Q(feedback__feedback_type=feedback_type))})
            elif annotate_field:
                posts = posts.annotate(**{annotate_field: Count('feedback')})

            # Order the queryset based on the annotated field
            if annotate_field and order_by == 'desc':
                annotate_field = '-' + annotate_field
                posts = posts.order_by(annotate_field)
            elif not annotate_field:  # If annotate_field is None, order by the specified field directly
                if order_by == 'desc':
                    sort_by = '-' + sort_by
                posts = posts.order_by(sort_by)
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
            return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
        else:
            # If no matching data is found, return an appropriate response
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)

class GetPost(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return PostCreateSerializer
        else:
            return PostSerializer

    @action(detail=False, methods=['GET'])
    def search_by_id(self, request, id):
        try:
            post = Post.objects.get(pk=id)
            serializer = PostSerializer(post)
            return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
        except Post.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
        
    @action(detail=False, methods=['PUT'])
    def update_post(self, request, id):
        try:
            post = Post.objects.get(pk=id)
            serializer = PostCreateSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
            else:
                return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST,  "BAD_REQUEST", serializer.errors)
        except Post.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
        
    @action(detail=False, methods=['DELETE'])
    def delete_post(self, request, id):
        try:
            post = Post.objects.get(pk=id)
            post.delete()
            return BaseAPIView.format_response(self, status.HTTP_204_NO_CONTENT, "Post deleted successfully.", None)
        except Post.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)

class RepliesView(generics.ListCreateAPIView):
    queryset = Reply.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RepliesCreateSerializer
        else:
            return RepliesSerializer

    def list(self, request, *args, **kwargs):
        posts = self.get_queryset()
        serializer = RepliesSerializer(posts, many=True)
        return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
    
    def post(self, request):
        try:
            serializer = RepliesCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return BaseAPIView.format_response(self, status.HTTP_201_CREATED, "CREATED", serializer.data)
            return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST,  "BAD_REQUEST", serializer.errors)
        except IntegrityError as e:
            return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST,  "BAD_REQUEST", serializer.errors)

class GetReply(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return RepliesCreateSerializer
        else:
            return RepliesSerializer

    @action(detail=False, methods=['GET'])
    def search_by_id(self, request, id):
        try:
            reply = Reply.objects.get(pk=id)
            serializer = RepliesSerializer(reply)
            return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
        except Reply.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
        
    @action(detail=False, methods=['PUT'])
    def update_reply(self, request, id):
        try:
            reply = Reply.objects.get(pk=id)
            serializer = RepliesCreateSerializer(reply, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
            else:
                return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST,  "BAD_REQUEST", serializer.errors)
        except Reply.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
        
    @action(detail=False, methods=['DELETE'])
    def delete_reply(self, request, id):
        try:
            reply = Reply.objects.get(pk=id)
            reply.delete()
            return BaseAPIView.format_response(self, status.HTTP_204_NO_CONTENT, "Replies deleted successfully.", None)
        except Reply.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)

class RepliesFeedbackView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = RepliesFeedback.objects.all()
    serializer_class = RepliesFeedbackSerializer

class PostFeedbackView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = PostFeedback.objects.all()
    serializer_class = PostFeedbackSerializer

class GetPostFeedbackView(viewsets.ModelViewSet):
    queryset = PostFeedback.objects.all()
    serializer_class = PostFeedbackSerializer

    @action(detail=False, methods=['GET'])
    def search_by_id(self, request, id):
        try:
            postFeedback = PostFeedback.objects.get(pk=id)
            serializer = PostFeedbackSerializer(postFeedback)
            return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
        except User.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
        
    @action(detail=False, methods=['PUT'])
    def update_feedback(self, request, id):
        try:
            postsFeedback = PostFeedback.objects.get(pk=id)
            serializer = PostFeedbackSerializer(postsFeedback, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
            else:
                return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST,  "BAD_REQUEST", serializer.errors)
        except Reply.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
        
class GetRepliesFeedbackView(viewsets.ModelViewSet):
    queryset = RepliesFeedback.objects.all()
    serializer_class = RepliesFeedbackSerializer

    @action(detail=False, methods=['GET'])
    def search_by_id(self, request, id):
        try:
            repliesFeedback = RepliesFeedback.objects.get(pk=id)
            serializer = RepliesFeedbackSerializer(repliesFeedback)
            return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
        except User.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
        
    @action(detail=False, methods=['PUT'])
    def update_feedback(self, request, id):
        try:
            repliesFeedback = RepliesFeedback.objects.get(pk=id)
            serializer = RepliesFeedbackSerializer(repliesFeedback, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return BaseAPIView.format_response(self, status.HTTP_200_OK, "OK", serializer.data)
            else:
                return BaseAPIView.format_response(self, status.HTTP_400_BAD_REQUEST,  "BAD_REQUEST", serializer.errors)
        except Reply.DoesNotExist:
            return BaseAPIView.format_response(self, status.HTTP_404_NOT_FOUND,  "Data Not Found", None)
        