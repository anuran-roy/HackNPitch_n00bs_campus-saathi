from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
class Issue(models.Model):
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

    # def get_absolute_url(self):
    #     return reverse('post',kwargs={'slug':self.slug})