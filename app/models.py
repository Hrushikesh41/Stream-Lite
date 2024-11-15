from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def set_password(self, raw_password):
        """Hashes the raw password and stores it."""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Checks if the provided password matches the stored hashed password."""
        return check_password(raw_password, self.password)

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='videos/')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)