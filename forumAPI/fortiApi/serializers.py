from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def save(self, **kwargs):
        # Automatically hash the password before saving
        self.validated_data['password'] = make_password(self.validated_data['password'], hasher='pbkdf2_sha256')
        super().save(**kwargs)

class RepliesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    post = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = '__all__'

    def get_likes(self, obj):
        return obj.get_total_likes()

    def get_dislikes(self, obj):
        return obj.get_total_dislikes()
    
    def get_user(self, obj):
        user = obj.user
        if user:
            return {'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'identity_number' : user.identity_number, 'username' : user.username}
        else :
            None
    
    def get_post(self, obj):
        post = obj.post
        if post:
            return {"id" : post.id, "content":post.content, "user_id": post.user_id}
        else :
            None

class RepliesCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = '__all__'

    def get_likes(self, obj):
        return obj.get_total_likes()

    def get_dislikes(self, obj):
        return obj.get_total_dislikes()

    def get_user_id(self, obj):
        user = obj.user
        if user:
            return {'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'identity_number' : user.identity_number, 'username' : user.username}
        else :
            None

    def get_post_id(self, obj):
        post = obj.post
        if post:
            return {"id" : post.id, "content":post.content, "user_id": post.user_id}
        else :
            None

class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    replies = RepliesSerializer(many=True, required=False, read_only=True)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_likes(self, obj):
        return obj.get_total_likes()

    def get_dislikes(self, obj):
        return obj.get_total_dislikes()

    def get_user(self, obj):
        user = obj.user
        if user:
            return {'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'identity_number' : user.identity_number, 'username' : user.username}
        else :
            None

class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_likes(self, obj):
        return obj.get_total_likes()

    def get_dislikes(self, obj):
        return obj.get_total_dislikes()

    def get_user(self, obj):
        user = obj.user
        if user:
            return {'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'identity_number' : user.identity_number, 'username' : user.username}
        else:
            return None
        
class PostCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField
    class Meta:
        model = Post
        fields = '__all__'

    def get_likes(self, obj):
        return obj.get_total_likes()

    def get_dislikes(self, obj):
        return obj.get_total_dislikes()

    def get_user_id(self, obj):
        user = obj.user
        if user:
            return {'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'identity_number' : user.identity_number, 'username' : user.username}
        else :
            None

class PostFeedbackSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    post_id = serializers.SerializerMethodField()  

    class Meta:
        model = PostFeedback
        fields = '__all__'
    
    def get_user_id(self, obj):
        user = obj.user
        if user:
            return {'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'identity_number' : user.identity_number, 'username' : user.username}
        else :
            None

    def get_post_id(self, obj):
        post = obj.post
        if post:
            return {"id" : post.id, "content":post.content, "user_id": post.user_id}
        else :
            None
    
class RepliesFeedbackSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    replies_id = serializers.SerializerMethodField()
    class Meta:
        model = RepliesFeedback
        fields = '__all__'

    def get_user_id(self, obj):
        user = obj.user
        return {'id' : user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'identity_number' : user.identity_number, 'username' : user.username}
    
    def get_replies_id(self, obj):
        replies = obj.replies
        return {"id" : replies.id, "content":replies.content, "user_id": replies.user_id}