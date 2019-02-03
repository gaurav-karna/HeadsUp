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
    path('login/', views.signIn, name='signIn'),
    path('postsign', views.postsign, name='postsign'),
    path('admin/welcome', views.admin_welcome, name='admin_welcome'),
    path('new_volunteer', views.volunteer_signup, name='new_volunteer'),
]
