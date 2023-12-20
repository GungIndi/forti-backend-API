from django.db import models

class User(models.Model):
    class UserRole(models.TextChoices):
        ADMIN = 'admin'
        HUMAS = 'humas'
        MAHASISWA = 'mahasiswa'
        DOSEN = 'dosen'
    first_name = models.CharField(max_length=32,null=True)
    last_name = models.CharField(max_length=32,null=True)
    identity_number = models.CharField(max_length=24, null=False, unique=True)
    username = models.CharField(max_length=32,null=False, unique=True)
    email = models.EmailField(max_length=32, null=False, default="")
    password = models.CharField(max_length=32)
    user_role = models.CharField(choices=UserRole.choices, null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Post(models.Model):
    user = models.ForeignKey(User, related_name='user_post',  on_delete=models.SET_NULL, null=True)
    content = models.TextField(blank=False, default="")
    category = models.CharField(max_length=32, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return f"{self.content}"
    
    def get_total_likes(self):
        return self.feedback.filter(feedback_type='like').count()

    def get_total_dislikes(self):
        return self.feedback.filter(feedback_type='dislike').count()
    
class Reply(models.Model):
    post = models.ForeignKey(Post, related_name='replies',  null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_reply', on_delete=models.SET_NULL, null=True)
    content = models.TextField(blank=False, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return f"{self.content}"
    
    def get_total_likes(self):
        return self.feedback.filter(feedback_type='like').count()

    def get_total_dislikes(self):
        return self.feedback.filter(feedback_type='dislike').count()

class PostFeedback(models.Model):
    class FeedbackType(models.TextChoices):
        LIKE = 'like'
        DISLIKE = 'dislike'

    user = models.ForeignKey(User, related_name='post_feedback', on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, related_name='feedback', on_delete=models.CASCADE, null=False, default='1')
    feedback_type = models.CharField(max_length=10, choices=FeedbackType.choices, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Feedback {self.feedback_type}"

class RepliesFeedback(models.Model):
    class FeedbackType(models.TextChoices):
        LIKE = 'like'
        DISLIKE = 'dislike'

    user = models.ForeignKey(User, related_name='replies_feedback', on_delete=models.SET_NULL, null=True)
    replies = models.ForeignKey(Reply,related_name='feedback', on_delete=models.CASCADE, null=False, default='1')
    feedback_type = models.CharField(max_length=10, choices=FeedbackType.choices, null=False, default="Like")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Feedback {self.feedback_type}"

