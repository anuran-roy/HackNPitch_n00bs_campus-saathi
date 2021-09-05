from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("<h1>This is the Home page!</h1>")
    return render(request, 'home/index.html')

def about(request):
    return HttpResponse("<h1>This is the About page!</h1>")

def team(request):
    return HttpResponse("<h1>This is the team page!</h1>")