from django.shortcuts import render, redirect, HttpResponse
from .models import Issue
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.defaultfilters import slugify

# Create your views here.
def index(request):
    params = {'issues': Issue.objects.all()}
    return render(request, 'forum/index.html', params)

def blogPost(request, slug):
    a = Issue.objects.filter(slug=slug)
    if list(a) == []:
        return HttpResponse("<h1>404 - Post not available!</h1>")
    else:
        params = dict(a.values()[0])
        return render(request, 'forum/issue.html', params)

def signup(request):
    if request.user.is_authenticated:
        return redirect('/forum/')
    else:
        return render(request, 'forum/signup.html')

def loggedin(request):
    if request.user.is_authenticated:
        return redirect('/forum/')
    else:
        return render(request, 'forum/login.html')

def newPost(request):
    if not request.user.is_authenticated:
        return redirect('/forum/login/')
    else:
        return render(request, 'forum/post.html')

def loginUser(request):
    if request.method == 'POST':    
        # return HttpResponse("<h1>This is the redirect page.<h1>")
        loginuser = request.POST.get('loginuser')
        loginpasswd = request.POST.get('loginpasswd')
        user = authenticate(username=loginuser, password=loginpasswd)

        if user is not None:
            login(request, user)
            return HttpResponse("<h1>Successfully logged in!</h1>")
        else:
            return HttpResponse("<h1>Credentials don't match.</h1>")
    else:
        return HttpResponse("<h1>HTTP 403 - Forbidden.</h1>")

def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponse("<h1>You've been successfully logged out.</h1>")

def newUser(request):
    if request.method == 'POST':    
        email = request.POST.get('email')
        password = request.POST.get('passwd', None)
        cpassword = request.POST.get('cpasswd', None)
        username = email[:email.find('@')]
        if cpassword == password:
            myuser = User.objects.create_user(username, email, password)
            # return HttpResponse("<h1>This is the redirect page.<h1>")
            myuser.first_name = request.POST.get('fname')
            myuser.last_name = request.POST.get('lname')
            myuser.middle_name = request.POST.get('mname', None)
            myuser.roll = request.POST.get('rollno')
            myuser.save()
            # messages.success(request, "Your account has been successfully created!")
            return HttpResponse("<h1>Your account has been successfully created!</h1>")
        else:
            return HttpResponse("<h1>Error - Passwords don't match.</h1>")
    else:
        return HttpResponse("<h1>HTTP 403 - Forbidden.</h1>")

def uploadPost(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        summary = request.POST.get('summary')
        description = request.POST.get('description')
        image = request.POST.get('image', None)

        author = request.user.username
        slug = slugify(f"{subject.lower()}-{author.lower()}")
        post = None
        if image is not None:
            post = Issue(subject=subject, summary=summary, description=description, image=image, author=author, slug=slug)
        else:
            post = Issue(subject=subject, summary=summary, description=description, author=author, slug=slug)
        post.save()
        return redirect('/forum/')
    else:
        return HttpResponse("<h1>HTTP 403 - Forbidden.</h1>")