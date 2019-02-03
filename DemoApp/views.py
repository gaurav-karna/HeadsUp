from django.shortcuts import render
from HeadsUpApp import views as heads_views
# Create your views here.

def index(request):
    locations = heads_views.get_locations()
    context = {
        'my_array':locations
    }
    return render(request, 'home.html', context)
