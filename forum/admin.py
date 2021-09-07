from django.contrib import admin
from .models import Issue, Comments

# Register your models here.
admin.site.register((Issue, Comments))
