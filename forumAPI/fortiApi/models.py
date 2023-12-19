from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    identity_number = models.CharField(max_length=19, null=False)
    user_name = models.CharField(max_length=30,null=False)
    email = models.EmailField(max_length=30, null=False, default="")
    password = models.CharField(max_length=32)
    USER_ROLE = models.TextChoices("userRole","admin humas mahasiswa dosen")
    user_role = models.CharField(choices=USER_ROLE.choices, null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class PostFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    FEEDBACK_TYPE = models.TextChoices("feedback","Like Dislike")
    feedback_type = models.CharField(choices=FEEDBACK_TYPE.choices, null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback {self.feedback_type}"
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    content = models.TextField(blank=False, default="")
    feedback = models.ForeignKey(PostFeedback, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Replied to Post {self.user}"

class RepliesFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    FEEDBACK_TYPE = models.TextChoices("feedback","Like Dislike")
    feedback_type = models.CharField(choices=FEEDBACK_TYPE.choices, null=False, default="Like")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback {self.feedback_type}"
    
class Reply(models.Model):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    content = models.TextField(blank=False, default="")
    feedback = models.ForeignKey(RepliesFeedback, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Replied to Post {self.post} by {self.user}"








class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=3)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.fullname