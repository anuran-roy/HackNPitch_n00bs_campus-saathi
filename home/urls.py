from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name="Home"),
    path('about/', views.about, name="About"),
    path('team/', views.team, name="Team"),

    # Error Page
    path('about/<str:id>/', views.errorPage, name="ErrorPage"),
    path('team/<str:id>/', views.errorPage, name="ErrorPage"),
]