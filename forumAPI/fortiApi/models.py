from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    identity_number = models.CharField(max_length=19, null=False)
    user_name = models.CharField(max_length=30,null=False)
    email = models.EmailField(max_length=30, null=False, default="")
    password = models.CharField(max_length=32)
    USER_ROLE = models.TextChoices("userRole","Admin Humas Mahasiswa Dosen")
    user_role = models.CharField(choices=USER_ROLE.choices, null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    content = models.TextField(null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user_name}"


class Reply(models.Model):
    post_id = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    content = models.TextField(null=False, default="")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Replied to Post {self.post_id} by {self.user_name}"


class PostFeedback(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    FEEDBACK_TYPE = models.TextChoices("feedback","Like Dislike")
    feedback_type = models.CharField(choices=FEEDBACK_TYPE.choices, null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback to Post {self.post_id} = {self.feedback_type}"

class RepliesFeedback(models.Model):
    replies_id = models.ForeignKey(Reply, on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    FEEDBACK_TYPE = models.TextChoices("feedback","Like Dislike")
    feedback_type = models.CharField(choices=FEEDBACK_TYPE.choices, null=False, default="Like")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback to Replies {self.replies_id} = {self.feedback_type}"



class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=3)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.fullname