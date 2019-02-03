from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
import threading
import pyrebase
# import time
import cv2
# import numpy as np

from . import db_methods as db_method


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

# Create your views here.

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