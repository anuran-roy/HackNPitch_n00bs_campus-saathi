from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, default="(Not available)")
    summary = models.TextField(max_length=200, default="(Not available)")
    description = models.TextField(max_length=750, default="(Not available)")
    image = models.ImageField(upload_to='forum/images/', blank=True)
    tracked = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), default=False)
    status = models.TextField(max_length=300, default="")
    date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=50, default="Anonymous")
    slug = models.SlugField(unique=True, max_length=100)
    votes = models.IntegerField(default=0)
    tvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-votes', '-date']

class Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, default='Anonymous')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    # votes = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255, default='testing')

    def __str__(self):
        return self.description[:50] + '...'

    class Meta:
        ordering = ['-timestamp'] # '-votes']

class UserProfile(models.Model):
    sno = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, default='Anonymous')
    reputation = models.IntegerField(default=0)
    rollno = models.CharField(max_length=20, default='')
    facebook = models.CharField(max_length=150, default='#')
    twitter = models.CharField(max_length=150, default='#')
    instagram = models.CharField(max_length=150, default='#')
    linkedin = models.CharField(max_length=150, default='#')

    def __str__(self):
        return self.username

# class TeacherProfile(models.Model):
