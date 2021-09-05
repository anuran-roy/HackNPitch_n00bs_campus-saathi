from django.shortcuts import render
from .models import Issue

# Create your views here.
def index(request):
    params = {'issues': Issue.objects.all()}
    
    return render(request, 'forum/index.html', params)