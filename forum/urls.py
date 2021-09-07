from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('post/<str:slug>', views.blogPost, name="PostView"),
    path('newpost/', views.newPost, name="NewPost"),
    path('login/', views.loggedin, name="Login"),
    path('signup/', views.signup, name="Signup"),
    path('newuser/', views.newUser, name="NewUser"),
    path('loginuser/', views.loginUser, name="LoginUser"),
    path('logout/', views.logoutUser, name="LogoutUser"),
    path('uploadpost/', views.uploadPost, name="UploadPost"),
    # path('user/<>')
]