from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'home.html', {})

def second(request):
    return render(request, 'second.html', {})
