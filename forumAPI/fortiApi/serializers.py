from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' 

class PostFeedbackSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    class Meta:
        model = PostFeedback
        fields = '__all__'

class RepliesFeedbackSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    class Meta:
        model = RepliesFeedback
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    feedback_id = RepliesFeedbackSerializer(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

class RepliesSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)
    feedback_id = PostFeedbackSerializer(read_only=True)
    class Meta:
        model = Reply
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__' 