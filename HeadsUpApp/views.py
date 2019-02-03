from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
import threading
import pyrebase
# import time
import cv2
from django.contrib.gis.geoip2 import GeoIP2
# import numpy as np

from .forms import *

from . import db_models as db_method


###########################-FIREBASE SETUP-##############################################

config = {
    "apiKey": "AIzaSyBOXMMnldokTRL1y6Je7sYGx8AFVkNRXRY",
    "authDomain": "smartglass-e01ec.firebaseapp.com",
    "databaseURL": "https://smartglass-e01ec.firebaseio.com",
    "storageBucket": "smartglass-e01ec.appspot.com"
}

# enabling important global variables
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

##########################################################################################

#---- Firebase authentication service ----#

def signIn(request):
    return render(request, "login.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email,passw)
    except:
        message = "Invalid credentials!"
        return render(request,"login.html",{"msg":message})
    return redirect('/admin/login')

#---- New Volunteer Signup----#

def volunteer_signup(request):
    if request.method == 'POST':
        ip = get_client_ip(request)
        g = GeoIP2()
        dataset = g.city(str(ip))
        # store new volunteer in Firebase
        vol_form = VolunteerForm(request.POST)
        if vol_form.is_valid():
            vol_data = {
                'First_Name':vol_form.cleaned_data['First_Name'],
                'Last_Name':vol_form.cleaned_data['Last_Name'],
                'Email':vol_form.cleaned_data['Email'],
                'Age':vol_form.cleaned_data['Age'],
                'Gender':vol_form.cleaned_data['Gender'],
                'Latitude':dataset.get('latitude', None),
                'Longitude':dataset.get('longitude', None)
            }
            # The .push method generates a unique timestamp key ; no need for hash
            db.child("Volunteers").push(vol_data)
            return render(request, 'thank_you.html', vol_data)
        return render(request, 'thank_you.html', {})
    else:
        context = {
            'profile_form':VolunteerForm()
        }
        return render(request, 'new_volunteer.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def confirm_volunteer(request):
#     email = request.POST.get('email')
#     passw = request.POST.get("pass")
#     try:
#         user = auth.sign_in_with_email_and_password(email, passw)
#     except:
#         message = "Invalid credentials!"
#         return render(request, "login.html", {"msg": message})
#     return redirect('/admin/login')

# returns a list of coordinates to be encoded into GeoJSON
def get_locations():
    location_list = []
    all_users = db.child("Volunteers").get()
    for user in all_users.each():
        pair = ((user.val().get('Latitude')), (user.val().get('Longitude')))
        if pair in location_list:
            pass
        else:
            location_list.append(pair)
    # location_list is a list of unique pairs of tuples denoting different locations
    return location_list

def encode_geoJSON (location_list):
    pass


###########################-ADMIN BASED VIEWS-##############################################

def admin_welcome(request):
    return render(request, 'admin_home.html', {})

def start_live(request):
    return render(request, 'live_feed.html', {})

def start_live_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace; boundary=frame")

# object that brings in the view from the drone

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


cam = VideoCamera()


def gen(camera):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')