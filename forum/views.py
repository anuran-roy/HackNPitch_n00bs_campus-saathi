from django.shortcuts import render, redirect, HttpResponse
from .models import Issue, Comment
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.defaultfilters import slugify
from random import randint
from datetime import datetime

# Create your views here.
def index(request):
    params = {'issues': Issue.objects.all()}
    return render(request, 'forum/index.html', params)

def search(request):
    return HttpResponse("<h1>Search function invoked!</h1>")

def blogPost(request, slug):
    issue = Issue.objects.filter(slug=slug)
    comments = Comment.objects.filter(issue=issue.first())
    if list(issue) == []:
        return HttpResponse("<h1>404 - Post not available!</h1>")
    else:
        params = dict(issue.values()[0])
        params["comments"] = comments
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
            return HttpResponse(f"<h1>Your account has been successfully created! Your username is: {myuser.username}. Save it somewhere.</h1>")
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

        comments_activity = list(Comment.objects.filter(username=request.user.username))
        params["comments"] = comments_activity
        print(params)
        # return HttpResponse(f"<h1>This will be the Dashboard for {request.user.username}</h1>")
        return render(request, 'forum/dashboard.html', params)
    else:
        return redirect('/forum/login')

def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postId = request.POST.get("postId")
        slug = request.POST.get("postSlug")
        issues = Issue.objects.get(id=postId)
        username = request.user.username
        # comment_slug = issue_slug + '-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        obj = Comment(description=comment, issue=issues, user=user, username=username, slug=slug)
        obj.save()
    else:
        return HttpResponse("<h1>HTTP 403 - Forbidden</h1>")
    return redirect(f'/forum/post/{slug}')

def voteUp(request):
    if request.method == 'POST':
        postId = request.POST.get("postId")
        issues = Issue.objects.filter(id=postId).first()
        slug = issues.slug
        # if num in [-1, 1] and list(issues) != []:
        issues.votes += 1
        issues.save()
    else:
        return HttpResponse("<h1>Forbidden</h1>")
    
    return redirect(f'/forum/post/{slug}')

def voteDown(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            postId = request.POST.get("postId")
            issues = Issue.objects.filter(id=postId).first()
            slug = issues.slug
            # if num in [-1, 1] and list(issues) != []:
            issues.votes -= 1
            issues.save()
        else:
            return HttpResponse("<h1>Forbidden</h1>")

        return redirect(f'/forum/post/{slug}')
    else:
        return redirect('/forum/login/')
    
