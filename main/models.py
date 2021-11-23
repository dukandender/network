from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

# User/profile model, contains additional information from the default user
class User(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.CharField(max_length=150, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='media/%Y/%m/%d',default='main/static/main/defaultavatar.png')
    following = models.ManyToManyField("User", blank=True, related_name="followers")
    def __str__(self):
        return f"User {self.username}"

# Post model that has owner,likes,location,etc. fields
class Post(models.Model):
    image = models.ImageField(upload_to='media/%Y/%m/%d',blank=False)
    text = models.CharField(max_length=2200)
    location = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.ManyToManyField(User, blank=True, related_name="likedposts")

    def __str__(self):
        return f"Post from {self.owner.first_name} at {self.location}"

class CommentManager(models.Manager):
    def create_comment(self,post,owner,text):
        comment = self.create(post=post,owner=owner,text=text)
        return comment

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=1600)
    
    objects = CommentManager()

    def __str__(self):
        return f"Comment from {self.owner.username} on {self.post}"

