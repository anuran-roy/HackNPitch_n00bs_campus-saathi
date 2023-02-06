from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('leaderboard/',views.StudentLeaderBoard, name="StudentLeaderBoard"),
    path('top-professors/', views.TeacherLeaderBoard, name="TeacherLeaderBoard"),

    # Post related APIs
    path('post/<str:slug>', views.blogPost, name="PostView"),
    path('newpost/', views.newPost, name="NewPost"),
    path('uploadpost/', views.uploadPost, name="UploadPost"),
    path('deletepost/<str:slug>', views.deletePost, name="Deletepost"),

    # Comment related APIs
    path('postcomment/', views.postComment, name="PostComment"),

    # Voting related APIs
    path('voteup/', views.voteUp, name="VoteUp"),
    path('votedown/', views.voteDown, name="VoteDown"),
    path('tvoteup/', views.tvoteUp, name="TVoteUp"),
    path('tvotedown/', views.tvoteDown, name="TVoteDown"),

    # Management related APIs
    path('login/', views.loggedin, name="Login"),
    path('signup/', views.signup, name="Signup"),
    path('newuser/', views.newUser, name="NewUser"),
    path('loginuser/', views.loginUser, name="LoginUser"),
    path('logout/', views.logoutUser, name="LogoutUser"),

    # Interface related APIs
    path('dashboard/', views.dashboard, name="Dashboard"),
    path('user/<str:slug>', views.userProfile, name="UserProfile"),

    # Search APIs
    path('search/', views.search, name="Search"),

    # Tag APIs
    path('tag/<str:slug>/', views.showTag, name="ShowTag"),

    # Error Page
    path('<str:id>/', views.errorPage, name="ErrorPage"),
]

api_patterns = [
    path("api/", include("forum.api_urls")),
]

urlpatterns += api_patterns