from django.db import models
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField

class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_courses')
    students = models.ManyToManyField(User, related_name='courses', blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Project(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = EmbedVideoField(blank=True)
    pdf_file = models.FileField(upload_to='pdfs/')
    github_url = models.URLField(blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    ai_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.author.username}"

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

