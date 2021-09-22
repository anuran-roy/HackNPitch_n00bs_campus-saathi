from django.shortcuts import render, redirect, HttpResponse
from .models import Issue, Comment, UserProfile, TeacherProfile, Tags
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.defaultfilters import slugify
from random import randint
from datetime import datetime
from .spamfilter import plino
from django.core.mail import send_mail

messages = {
    "404": {
        "code": 404,
        "status": "Page not found",
        "message": "Oops! The page you are looking for does not exist. It might have been moved or deleted."
    },
    "403": {
        "code": 403,
        "status": "Forbidden",
        "message": '"Tresspassers will be prosecuted." ~ Developers'
    },
    "500": {
        "code": 500,
        "status": "Server Error",
        "message": ""
    },
}

# Create your views here.

##################################################### For index and error pages #####################################################

def index(request):
    if request.user.is_authenticated:
        params = {'issues': Issue.objects.all()}
        params["page_title"] = "Posted Issues"
        return render(request, 'forum/index.html', params)
    else:
        return redirect('/forum/login')


def errorPage(request, args=messages["404"], **kwargs):
    return render(request, 'forum/errorpage.html', args)

##################################################### End index and error pages #####################################################

##################################################### For User authentication and related activities #####################################################


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
        return errorPage(request, messages["403"])


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

        image = request.FILES.get('profilepic')

        print(f"\n\n\n\n{role}\n\n")
        print(f"\n\n\n\n{User.objects.all()}\n\n")
        try:    
            if cpassword == password:
                myuser = User.objects.create_user(username, email, password)
                print(f"\n\n\n\n{myuser.__dict__}\n\n")
                # return HttpResponse("<h1>This is the redirect page.<h1>")
                myuser.first_name = request.POST.get('fname')
                myuser.last_name = request.POST.get('lname')
                myuser.middle_name = request.POST.get('mname', None)
                # myuser.roll = request.POST.get('rollno')
                # myuser.reputation = 0
                myuser.save()
                myprofile = None
                if role == 'student':
                    myprofile = UserProfile(reputation=0, rollno = request.POST.get('rollno'), user=myuser, username=username, profilepic=image)
                elif role == 'teacher':
                    myprofile = TeacherProfile(reputation=0, rollno = request.POST.get('rollno'), user=myuser, username=username, tags=[{"tags": []}], profilepic=image)

                print(f"\n\n\n\n{myprofile.__dict__}\n\n")
                myprofile.save()

                # authenticate(username=username, password=password)
                # messages.success(request, "Your account has been successfully created!")
                # return HttpResponse(f"<h1>Your account has been successfully created! Your username is: {myuser.username}. Save it somewhere.</h1>")
                msg = {
                    "code": "Welcome!",
                    "status": "Congratulations! Your account has been created!",
                    "message": f"Your account has been successfully created! Your username is: {myuser.username}. Save it somewhere."
                    }
                return errorPage(request, msg)
                # return redirect('/forum/dashboard')
            elif cpassword != password:
                # return HttpResponse("<h1>Error - Passwords don't match.</h1>")
                msg = {
                    "code": "Error",
                    "status": "Uh oh! Your passwords don't match :(",
                    "message": "Try signing up again, with matching passwords. No worries - we'll be waiting! :D"
                    }
                return errorPage(request, msg)
            elif User.objects.filter(username=username) is not None:
                return redirect('/forum/login')
        except Exception as e:
            msg = {
                    "code": "Error",
                    "status": "Houston! We've got a problem! :(",
                    "message": f"Please Report the administration about the problem as soon as possible! Tell them the error: {e.message}"
                }
            return errorPage(request, msg)
            # return HttpResponse(f"<h1>An Error Occured. Error details: {e}</h1>")
    else:
        return errorPage(request, messages["403"])


def passwordReset(request):
    return HttpResponse("<h1>Password Reset</h1>")

# def sendMessage(message, args={}):


# def verifyCode(request, slug):
#     num = 

##################################################### End User authentication and related activities #####################################################

##################################################### For User Activities #####################################################

def blogPost(request, slug):
    try:
        issue = Issue.objects.filter(slug=slug)
        comments = Comment.objects.filter(issue=issue.first())
        if list(issue) == []:
            # return HttpResponse("<h1>404 - Post not available!</h1>")
            return errorPage(request, message["404"])
        else:
            params = dict(issue.values()[0])
            print(f"\n\n\n{params}\n\n\n")
            params["comments"] = comments
            return render(request, 'forum/issue.html', params)
    except Exception as e:
        return errorPage(request, messages["404"])

def newPost(request):
    if not request.user.is_authenticated:
        return redirect('/forum/login/')
    else:
        return render(request, 'forum/post.html')


def uploadPost(request):
    if request.method == "POST":
        user = request.user
        subject = request.POST.get('subject')
        summary = request.POST.get('summary')
        description = request.POST.get('description')

        # if plino(description):
        #     return HttpResponse("<h1>Really very very sorry fam,<br>your comment has been marked as spam.</h1>")
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
        return errorPage(request, messages["403"])


def userProfile(request, slug):
    try:
        user = User.objects.filter(username=slug)
        user_issues = Issue.objects.filter(author=slug)

        params = dict(user.values()[0])
        params["user_issues"] = list(user_issues.values())
        params["comments"] = list(Comment.objects.filter(username=slug).values())

        profileType = None
        profilepic = ''

        if UserProfile.objects.filter(username=slug).exists():
            profileType = "Student"
            profilepic = UserProfile.objects.filter(username=slug).first().profilepic
        elif TeacherProfile.objects.filter(username=slug).exists():
            profileType = "Faculty"
            profilepic = TeacherProfile.objects.filter(username=slug).first().profilepic
        else:
            profileType = "Unknown"
        
        params["profileType"] = profileType
        params["profilepic"] = profilepic

        if list(user) == []:
            msg = {
                    "code": 404,
                    "status": "Username not found :(",
                    "message": f"The username {slug} you've been searching for is not available in our data. :( Maybe the user deleted their account, or is Anonymous?"
                }
            return errorPage(request, msg)
            # return HttpResponse("<h1>Username not found!</h1>")
        elif request.user.username == slug:
            return redirect('/forum/dashboard/')
        else:
            return render(request, 'forum/user.html', params)
    except IndexError:
        # return HttpResponse("<h1>Username not found!</h1>")
        msg = {
                "code": 404,
                "status": "Username not found :(",
                "message": f"The username {slug} you've been searching for is not available in our data. :( Maybe the user deleted their account, or is Anonymous?"
            }
        return errorPage(request, msg)


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
        params["profilepic"] = profile.__dict__["profilepic"] if not request.user.is_superuser else ''
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
            ls2 = [x.label for x in ls]

            if myprof is not None:
                myprof.tags = ls2
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
        # print("\n\n\n\n" + postId + str(type(postId)) + "\n\n\n")
        slug = request.POST.get("postSlug")
        issues = Issue.objects.filter(sno=postId).first()
        username = request.user.username
        tags = TagsProcessor(request, "comment", {"author": username, "slug": slug})

        # comment_slug = issue_slug + '-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        if not plino(comment):
            obj = Comment(description=comment, issue=issues, user=user, username=username, slug=slug, tags=tags)
            obj.save()
            return redirect(f'/forum/post/{slug}')
        else:
            msg = {
                    "code": "Spam",
                    "status": "Spam detected",
                    "message": "Really very very sorry fam,<br>your comment has been marked as spam."
                }
            return errorPage(request, msg)
    else:
        # return HttpResponse("<h1>HTTP 403 - Forbidden</h1>")
        return errorPage(request)


def deletePost(request, slug):
    if request.method == "POST":
        postId = request.POST.get("postId")
        author = request.POST.get("poster")
        postSlug = None
        a = None
        if slug == "issue":
            a = Issue.objects.filter(sno=postId).first()
            print(f"\n\nPost: \n\n{a}\n\n")
        elif slug == "comment":
            a = Comment.objects.filter(sno=postId).first()
            print(f"\n\nComment: \n\n{a}\n\n")
        postSlug = str(a.slug)
        print(f"\n\n{request.user.username}")
        print(f"\n\n{author}")
        if request.user.username == author or request.user.is_superuser:
            a.delete()
            if slug == "issue":
                return redirect("/forum/")
            elif slug == "comment":
                return redirect(f"/forum/post/{postSlug}")
        else:
            msg = dict(messages["403"])
            msg["message"] = "Hippity hoppity floppity, the post isn't your property :P"
            return errorPage(request, msg)
            # return HttpResponse("<h1>Hippity hoppity floppity, the post isn't your property :P")
    else:
        return errorPage(request, messages["403"])

##################################################### End User Activities #####################################################

##################################################### For voting #####################################################

def voteUp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            postId = request.POST.get("postId")
            author = request.POST.get("poster")
            issues = Issue.objects.filter(sno=postId).first()
            user = User.objects.filter(username=author).first()
            userprofile = None # list(set([TeacherProfile.objects.filter(username=author).first(), UserProfile.objects.filter(username=author).first()]))[0]  # if not (user.is_superuser or user.is_staff) else None
            if TeacherProfile.objects.filter(username=author).first() is not None:
                userprofile = TeacherProfile.objects.filter(username=author).first()
            else:
                userprofile = UserProfile.objects.filter(username=author).first()
            # print("UserProfile:", userprofile.__dict__)
            # print("\n\nUser:", user.__dict__)
            slug = issues.slug
            # if num in [-1, 1] and list(issues) != []:
            issues.votes += 1
            if user is not None and author != "Anonymous" and user.is_superuser == False and user.is_staff == False:
                userprofile.reputation -= 1
                userprofile.save()
            issues.votes -= 1
            issues.save()
            user.save()
        else:
            return errorPage(request, messages["403"])
        
        return redirect(f'/forum/post/{slug}')
    else:
        return redirect('/forum/login/')


def voteDown(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            postId = request.POST.get("postId")
            author = request.POST.get("poster")
            issues = Issue.objects.filter(sno=postId).first()
            user = User.objects.filter(username=author).first()
            # print(f"\n\n{user}\n\n")
            userprofile = None # list(set([TeacherProfile.objects.filter(username=author).first(), UserProfile.objects.filter(username=author).first()]))[0]  # if not (user.is_superuser or user.is_staff) else None
            if TeacherProfile.objects.filter(username=author).first() is not None:
                userprofile = TeacherProfile.objects.filter(username=author).first()
            else:
                userprofile = UserProfile.objects.filter(username=author).first()
            # print(f"\n\n{userprofile}\n\n")
            # print("UserProfile:", userprofile.__dict__)
            # print("\n\nUser:", user.__dict__)
            slug = issues.slug
            # if num in [-1, 1] and list(issues) != []:
            if user is not None and author != "Anonymous" and user.is_superuser == False and user.is_staff == False:
                userprofile.reputation -= 1
                userprofile.save()
            issues.votes -= 1
            issues.save()
            user.save()
            
        else:
            return errorPage(request, messages["403"])
        
        return redirect(f'/forum/post/{slug}')
    else:
        return redirect('/forum/login/')


def tvoteUp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # postId = request.POST.get("postId")
            tags = eval(request.POST.get("postTags"))
            print(f"\n\n\n{tags}\t{type(tags)}\n\n\n")
            # issues = Issue.objects.filter(id=postId).first()
            # user = User.objects.filter(username=author).first()
            usernames_list = []
            # teachers_list = []
            for tagname in tags:
                print(f"\n{tagname}\n")
                usernames_list += Tags.objects.filter(label=tagname).first().usernames
            
            usernames_list = list(set(usernames_list))
            print(f"\n{usernames_list}\n")

            for i in usernames_list:
                print(f"\n{i}\n")
                teacheruser = TeacherProfile.objects.filter(username=i).first()
                print(f"\n{teacheruser}\n")
                if teacheruser is not None:
                    teacheruser.reputation += 1
                    teacheruser.save()

            # return HttpResponse("Don't you think the authorities are awesome? :D")
            msg = {
                "code": ":)",
                "status": "Kudos to the authorities!",
                "message": "Your upvote has been successfully recorded. Don't you think the authorities are awesome? :D",
            }
            return errorPage(request, msg)
        else:
            msg = dict(messages["403"])
            msg["message"] = '"There are no shortcuts to votes :)" ~ Developers'
            return errorPage(request, msg)
    else:
        return redirect('/forum/login')


def tvoteDown(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # postId = request.POST.get("postId")
            tags = eval(request.POST.get("postTags"))
            print(f"\n\n\n{tags}\t{type(tags)}\n\n\n")
            # issues = Issue.objects.filter(id=postId).first()
            # user = User.objects.filter(username=author).first()
            usernames_list = []
            # teachers_list = []
            for tagname in tags:
                print(f"\n{tagname}\n")
                usernames_list += Tags.objects.filter(label=tagname).first().usernames
            
            usernames_list = list(set(usernames_list))
            print(f"\n{usernames_list}\n")

            for i in usernames_list:
                print(f"\n{i}\n")
                teacheruser = TeacherProfile.objects.filter(username=i).first()
                print(f"\n{teacheruser}\n")
                if teacheruser is not None:
                    teacheruser.reputation -= 1
                    teacheruser.save()

            msg = {
                "code": ":(",
                "status": "So sorry to know that...",
                "message": "Your downvote has been successfully recorded. Maybe they'll look into it now?",
            }
            return errorPage(request, msg)
            # return HttpResponse("So sorry to know that :(... Maybe they'll look into it now?")
        else:
            # return HttpResponse('"There are no shortcuts to votes :)" ~ Developers')
            msg = dict(messages["403"])
            msg["message"] = '"There are no shortcuts to votes :)" ~ Developers'
            return errorPage(request, msg)
    else:
        return redirect('/forum/login')


##################################################### End voting #####################################################

##################################################### For search and leaderboards #####################################################

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


##################################################### End search and leaderboards #####################################################

##################################################### For tags #####################################################

def TagsProcessor(request, mode, args):

    text = request.POST.get("tags")

    taglist = list(set([slugify(x.strip(" ").strip("&nbsp;").lower()) for x in text.strip(" ").strip("&nbsp;").split(",")]))

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
        msg = dict(messages["404"])
        msg["status"] = "That's the wrong way."
        msg["message"] = f"Tag '{slug}' doesn't exist. It may have been deleted, or might have never existed."
        return errorPage(request, msg)
        


##################################################### End tags #####################################################
