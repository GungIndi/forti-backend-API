from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    USER_ROLE = models.TextChoices("userRole","Admin Humas Mahasiswa Dosen")
    user_role = models.CharField(max_length = 10, choices=USER_ROLE.choices, null = False)
    created_at = models.DateTimeField(auto_now=True)

class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=3)
    mobile = models.CharField(max_length=15)

class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True, unique=True),
    created_at = models.DateField(auto_now=True)

class Replies(models.Model):
    replies_id = models.BigAutoField(primary_key=True, unique=True),
    created_at = models.DateField(auto_now_add=True)

class Feedback(models.Model):
    feedback_id = models.BigAutoField(primary_key=True, unique=True),
    created_at = models.DateField(auto_now_add=True)
