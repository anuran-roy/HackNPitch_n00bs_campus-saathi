from django.shortcuts import render, HttpResponse
from .models import Issue

# Create your views here.
def index(request):
    params = {'issues': Issue.objects.all()}
    return render(request, 'forum/index.html', params)

def blogPost(request, slug):
    a = Issue.objects.filter(slug=slug)
    if list(a) == []:
        return HttpResponse("Post not available!")
    else:
        params = dict(a.values()[0])
        return render(request, 'forum/issue.html', params)

    