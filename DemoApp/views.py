from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'home.html', {})

def devpost(request):
    return redirect('https://devpost.com/')

def team(request):
    return render(request, 'team.html', {})
