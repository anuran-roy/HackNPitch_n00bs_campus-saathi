from django.shortcuts import render, HttpResponse

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
def index(request):
    # return HttpResponse("<h1>This is the Home page!</h1>")
    return render(request, 'home/index.html')

def about(request):
    return HttpResponse("<h1>This is the About page!</h1>")

def team(request):
    return HttpResponse("<h1>This is the team page!</h1>")

def errorPage(request, args=messages["404"], **kwargs):
    return render(request, 'home/errorpage.html', args)