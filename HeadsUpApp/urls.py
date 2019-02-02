from django.urls import path, include
from . import views

'''
# import django.contrib.auth
# from django.conf import settings
# import django.contrib.auth.views as auth_views
'''

urlpatterns = [
    path('live', views.start_live, name='start_live'),
    path('live/feed', views.start_live_feed, name='live_feed'),

]
