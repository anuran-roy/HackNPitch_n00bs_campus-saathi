from django.db import models

# Create your models here.
class Issue(models.Model):
    subject = models.CharField(max_length=100, default="(Not available)")
    summary = models.TextField(max_length=200, default="(Not available)")
    description = models.TextField(max_length=750, default="(Not available)")
    image = models.ImageField(upload_to='forum/images', default="")
    tracked = models.BooleanField(choices=((True, 'Yes'), (False, 'No')), default=False)
    date = models.DateField(auto_now_add=True)
    author = models.CharField(max_length=50, default="Anonymous")

    def __str__(self):
        return self.subject