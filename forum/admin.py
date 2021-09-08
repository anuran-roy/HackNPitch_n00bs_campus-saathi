from django.contrib import admin
from .models import Issue, Comment

# Register your models here.
admin.site.register((Issue, Comment))
