from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Issue(models.Model):
    sno = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100, default="(Not available)")
    summary = models.TextField(max_length=200, default="(Not available)")
    description = models.TextField(max_length=750, default="(Not available)")
    image = models.ImageField(upload_to='forum/images/', blank=True)
    tracked = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), default=False)
    status = models.TextField(max_length=300, default="")
    date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=50, default="Anonymous")
    slug = models.SlugField(unique=True, max_length=100)

    def __str__(self):
        return self.subject

class Comments(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:50] + '...'