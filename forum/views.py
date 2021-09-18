from django.shortcuts import render, redirect, HttpResponse
from .models import Issue, Comment, UserProfile, TeacherProfile, Tags
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.defaultfilters import slugify
from random import randint
from datetime import datetime
from .spamfilter import plino

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        params = {'issues': Issue.objects.all()}
        params["page_title"] = "Posted Issues"
        return render(request, 'forum/index.html', params)
    else:
        return redirect('/forum/login')

def search(request):
    return HttpResponse("<h1>Search function invoked!</h1>")

def blogPost(request, slug):
    issue = Issue.objects.filter(slug=slug)
    comments = Comment.objects.filter(issue=issue.first())
    if list(issue) == []:
        return HttpResponse("<h1>404 - Post not available!</h1>")
    else:
        params = dict(issue.values()[0])
        print(f"\n\n\n{params}\n\n\n")
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
        username = email
        role = request.POST.get('role', 'student')
        if cpassword == password and User.objects.filter(username=username) is None:
            myuser = User.objects.create_user(username, email, password)

            # return HttpResponse("<h1>This is the redirect page.<h1>")
            myuser.first_name = request.POST.get('fname')
            myuser.last_name = request.POST.get('lname')
            myuser.middle_name = request.POST.get('mname', None)
            # myuser.roll = request.POST.get('rollno')
            # myuser.reputation = 0
            myuser.save()
            
            if role == 'student':
                myprofile = UserProfile(reputation=0, rollno = request.POST.get('rollno'), user=myuser, username=username)
            elif role == 'teacher':
                myprofile = TeacherProfile(reputation=0, empno = request.POST.get('rollno'), user=myuser, username=username, tags=[{"tags": []}])
            myprofile.save()

            authenticate(username=username, password=password)
            # messages.success(request, "Your account has been successfully created!")
            # return HttpResponse(f"<h1>Your account has been successfully created! Your username is: {myuser.username}. Save it somewhere.</h1>")
            return redirect('/forum/dashboard')
        elif cpassword != password:
            return HttpResponse("<h1>Error - Passwords don't match.</h1>")
        elif User.objects.filter(username=username) is not None:
            return redirect('/forum/login')
    else:
        return HttpResponse("<h1>HTTP 403 - Forbidden.</h1>")

def uploadPost(request):
    if request.method == "POST":
        user = request.user
        subject = request.POST.get('subject')
        summary = request.POST.get('summary')
        description = request.POST.get('description')
        image = request.FILES.get('myfile')
        is_anonymous = request.POST.get("anonymize", "off")
        # print(image)
        author = request.user.username if is_anonymous == "off" else "Anonymous"
        slug = slugify(f"{subject.lower()}-{author.lower()}")

        tags = TagsProcessor(request, "post", {"author": author, "slug": slug})

        post = None
        if image is not None:
            post = Issue(user=user, subject=subject, summary=summary, description=description, image=image, author=author, slug=slug, tags=tags)
        else:
            post = Issue(user=user, subject=subject, summary=summary, description=description, author=author, slug=slug, tags=tags)
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
        activity = list(Issue.objects.filter(user=request.user))
        data = User.objects.filter(username = request.user.username)
        profile = UserProfile.objects.filter(username = request.user.username).first()

        if request.user.is_superuser:
            return redirect("/admin/")
        isTeacher = False

        if(profile == None):
            profile = TeacherProfile.objects.filter(username = request.user.username).first()
            isTeacher = True

        params = dict(data.values()[0])
        params["activity"] = activity
        params["rollno"] = profile.__dict__["rollno"] if not request.user.is_superuser else "NA"
        params["reputation"] = profile.__dict__["reputation"] if not request.user.is_superuser else "Inf"

        if isTeacher:
            params["tags"] = profile.__dict__["tags"]

        comments_activity = list(Comment.objects.filter(username=request.user.username))
        params["comments"] = comments_activity
        # print(params)
        # return HttpResponse(f"<h1>This will be the Dashboard for {request.user.username}</h1>")
        if isTeacher:
            a = list(Tags.objects.all())
            username = request.user.username
            ls = []
            
            for i in a:
                if username in i.usernames:
                    ls.append(i)
            
            params["notifications"] = ls
            myprof = TeacherProfile.objects.filter(username=username).first()
            ls2 = [i.label for i in ls]
            myprof.tags["tags"] = ls2
            myprof.save()
            
            print(f"\n\n\n{ls}\n\n\n")

        if isTeacher:
            return render(request, 'forum/staff/dashboard.html', params)
        else:
            return render(request, 'forum/student/dashboard.html', params)
    else:
        return redirect('/forum/login')


def postComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        postId = request.POST.get("postId")
        print("\n\n\n\n" + postId + str(type(postId)) + "\n\n\n")
        slug = request.POST.get("postSlug")
        issues = Issue.objects.filter(sno=postId).first()
        username = request.user.username
        tags = TagsProcessor(request, "comment", {"author": username, "slug": slug})

        # comment_slug = issue_slug + '-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        if not plino(comment):
            obj = Comment(description=comment, issue=issues, user=user, username=username, slug=slug)
            obj.save()
        else:
            return HttpResponse("<h1>Really very very sorry fam,<br>your comment has been marked as spam.</h1>")
    else:
        return HttpResponse("<h1>HTTP 403 - Forbidden</h1>")
    return redirect(f'/forum/post/{slug}')


def voteUp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            postId = request.POST.get("postId")
            author = request.POST.get("poster")
            issues = Issue.objects.filter(id=postId).first()
            user = User.objects.filter(username=author).first()
            userprofile = UserProfile.objects.filter(username=author).first() if not (user.is_superuser or user.is_staff) else None
            # print("UserProfile:", userprofile.__dict__)
            # print("\n\nUser:", user.__dict__)
            slug = issues.slug
            # if num in [-1, 1] and list(issues) != []:
            issues.votes += 1
            if user is not None and author != "Anonymous":
                userprofile.reputation += 1
            issues.save()
            user.save()
            userprofile.save()
        else:
            return HttpResponse("<h1>Forbidden</h1>")
        
        return redirect(f'/forum/post/{slug}')
    else:
        return redirect('/forum/login/')

def voteDown(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            postId = request.POST.get("postId")
            author = request.POST.get("poster")
            issues = Issue.objects.filter(id=postId).first()
            user = User.objects.filter(username=author).first()
            userprofile = UserProfile.objects.filter(username=author).first() if not (user.is_superuser or user.is_staff) else None
            # print("UserProfile:", userprofile.__dict__)
            # print("\n\nUser:", user.__dict__)
            slug = issues.slug
            # if num in [-1, 1] and list(issues) != []:
            if user is not None and author != "Anonymous":
                issues.votes -= 1
                userprofile.reputation -= 1
            issues.save()
            user.save()
            userprofile.save()
        else:
            return HttpResponse("<h1>Forbidden</h1>")
        
        return redirect(f'/forum/post/{slug}')
    else:
        return redirect('/forum/login/')

def tvoteUp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            postId = request.POST.get("postId")
            author = request.POST.get("poster")
            issues = Issue.objects.filter(id=postId).first()
            user = User.objects.filter(username=author).first()
    
def search(request):
    issues = list(Issue.objects.all())
    query = request.POST.get('search')

    results_list = []

    init = datetime.now()
    for i in issues:
        idict = i.__dict__

        for j in idict.keys():
            if j != '_state':
                if isinstance(idict[j],str):
                    if query.lower() in idict[j].lower():
                        results_list.append(i)
    
    results_list = list(set(results_list))
    params = {'issues': results_list}
    params["page_title"] = f"Showing {len(results_list)} search results for '{query}' in {(datetime.now() - init).total_seconds()} seconds"
    return render(request, 'forum/index.html', params)

def StudentLeaderBoard(request):
    users = list(UserProfile.objects.all())
    users.sort(key = lambda x: x.reputation, reverse=True)
    params = {}
    params["page_title"] = "Student Leaderboard"
    params["users"] = users
    return render(request, 'forum/student/leaderboard.html', params)

def TeacherLeaderBoard(request):
    users = list(TeacherProfile.objects.all())
    users.sort(key = lambda x: x.reputation, reverse=True)
    params = {}
    params["page_title"] = "Staff Leaderboard"
    params["users"] = users
    return render(request, 'forum/staff/leaderboard.html', params)

# def getTags(request, param)

def TagsProcessor(request, mode, args):

    text = request.POST.get("tags")

    taglist = list(set([slugify(x.strip(" ").lower()) for x in text.strip(" ").split(",")]))

    tags_all = [x.label for x in Tags.objects.all()]

    username = request.user.username

    if mode == "post":
        for i in taglist:
            if i not in tags_all:
                newtag = Tags(label=i, usernames=[], issues=[], comments=[])
                newtag.save()

        i = taglist[0]

        for i in taglist:
            a = Tags.objects.filter(label=i).first()
            a.issues.append(args["slug"])
            a.usernames.append(args["author"])
            a.usernames = list(set(a.usernames))
            a.issues = list(set(a.issues))            
            a.save()
    
    elif mode == "comment":
        for i in taglist:
            if i not in tags_all:
                newtag = Tags(label=i, usernames=[], issues=[], comments=[])
                newtag.save()
        
        i = taglist[0]

        for i in taglist:
            a = Tags.objects.filter(label=i).first()
            a.comments.append(args["slug"])
            a.usernames.append(args["author"])
            a.usernames = list(set(a.usernames))
            a.comments = list(set(a.comments))
            a.save()

    return taglist

def showTag(request, slug):
    tags = Tags.objects.filter(label=slug).first()
    if tags is not None: 
        # return HttpResponse(f"<h1>This is the tag page of {slug}</h1>")
        return render(request, 'forum/tag.html', tags.__dict__)
    else:
        return HttpResponse(f"<h1>Tag {slug} doesn't exist!</h1>")