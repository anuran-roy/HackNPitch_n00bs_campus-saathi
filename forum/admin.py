from django.contrib import admin
from .models import Issue, Comment, UserProfile, TeacherProfile

# Register your models here.
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(TeacherProfile)