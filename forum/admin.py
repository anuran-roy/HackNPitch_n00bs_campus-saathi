from django.contrib import admin
from .models import Issue, Comment, UserProfile

# Register your models here.
admin.site.register((Issue, Comment, UserProfile))
