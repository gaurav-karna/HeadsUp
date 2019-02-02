from django.urls import path, include
from . import views

'''
# import django.contrib.auth
# from django.conf import settings
# import django.contrib.auth.views as auth_views
'''

urlpatterns = [
    path('', views.index, name='home_page'),
]