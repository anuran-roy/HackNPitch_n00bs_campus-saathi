from django.shortcuts import render, redirect, HttpResponse
from .models import Issue, Comment
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.defaultfilters import slugify
from random import randint

# Create your views here.
def index(request):
    params = {'issues': Issue.objects.all()}
    return render(request, 'forum/index.html', params)

def search(request):
    return HttpResponse("<h1>Search function invoked!</h1>")

def blogPost(request, slug):
    post = Issue.objects.filter(slug=slug)
    # comments = Comment.objects.filter(post=post.first())
    if list(post) == []:
        return HttpResponse("<h1>404 - Post not available!</h1>")
    else:
        params = dict(post.values()[0])
        # params["comments"] = comments
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
            return redirect('/forum/dashboard/')
        else:
            return HttpResponse("<h1>Credentials don't match.</h1>")
    else:
        return HttpResponse("<h1>HTTP 403 - Forbidden.</h1>")

def logoutUser(request):
    # if request.method == 'POST':
    logout(request)
    # return HttpResponse("<h1>You've been successfully logged out.</h1>")
    return redirect('/forum/')

def newUser(request):
    if request.method == 'POST':    
        email = request.POST.get('email')
        password = request.POST.get('passwd', None)
        cpassword = request.POST.get('cpasswd', None)
        username = slugify(email[:email.find('@')].lower()+'-'+str(randint(1,10000)))
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
        image = request.FILES.get('myfile')
        print(image)
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

def userProfile(request, slug):
    try:
        user = User.objects.filter(username=slug)
        user_issues = Issue.objects.filter(author=slug)
        params = dict(user.values()[0])
        params["user_issues"] = list(user_issues.values())
        if list(user) == []:
            return HttpResponse("<h1>Username not found!</h1>")
        elif request.user.username == slug:
            return redirect('/forum/dashboard/')
        else:
            return render(request, 'forum/user.html', params)
    except IndexError:
        return HttpResponse("<h1>Username not found!</h1>")

def dashboard(request):
    if request.user.is_authenticated:
        activity = list(Issue.objects.filter(author=request.user.username))
        data = User.objects.filter(username = request.user.username)
        params = dict(data.values()[0])
        params["activity"] = activity
        # return HttpResponse(f"<h1>This will be the Dashboard for {request.user.username}</h1>")
        return render(request, 'forum/dashboard.html', params)
    else:
        return redirect('/forum/login')

def postComment(request, slug):
    if request.method == 'POST':
        # sno = 
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("issueSno")
        issues = Issue.objects.get(sno=postSno)
    else:
        pass
    return redirect(f'/forum/post/{slug}')