from django.db import models

# Create your models here.
class ContactModel(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    phone = models.BigIntegerField(blank=True)
    message = models.TextField(blank=False)

    def __str__(self):
        return self.name