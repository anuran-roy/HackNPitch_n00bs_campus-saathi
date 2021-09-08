from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),

    # Post related APIs
    path('post/<str:slug>', views.blogPost, name="PostView"),
    path('newpost/', views.newPost, name="NewPost"),
    path('uploadpost/', views.uploadPost, name="UploadPost"),

    # Comment related APIs
    path('postcomment/', views.postComment, name="PostComment"),

    # Management related APIs
    path('login/', views.loggedin, name="Login"),
    path('signup/', views.signup, name="Signup"),
    path('newuser/', views.newUser, name="NewUser"),
    path('loginuser/', views.loginUser, name="LoginUser"),
    path('logout/', views.logoutUser, name="LogoutUser"),

    # Interface related APIs
    path('dashboard/', views.dashboard, name="Dashboard"),
    path('user/<str:slug>', views.userProfile, name="UserProfile"),
]