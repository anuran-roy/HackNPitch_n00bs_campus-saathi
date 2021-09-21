from django.contrib import admin
from .models import Issue, Comment, UserProfile, TeacherProfile, Tags

# Register your models here.
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(TeacherProfile)
admin.site.register(Tags)