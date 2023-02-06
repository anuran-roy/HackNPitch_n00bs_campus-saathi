from django.contrib import admin
from django.urls import path, include

from . import api_views

urlpatterns = [
    path("issues/", api_views.get_issues, name="get_issues"),
]
