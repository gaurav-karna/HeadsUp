from .db_models import Volunteer, Admin
from django import forms
from django.db import models
# Volunteer Form

class VolunteerForm(forms.Form):

    model = Volunteer

    genders = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Rather Not Say', 'Rather Not Say')
    )

    First_Name = forms.CharField(max_length=32, required=True)
    Last_Name = forms.CharField(max_length=32, required=True)
    Email = forms.EmailField(required=True)
    Age = forms.IntegerField(max_value=75, min_value=13, required=True)
    Gender = forms.ChoiceField(choices=genders, required=True)

    class Meta:
        fields = [
            'First_Name',
            'Last_Name',
            'Email',
            'Age',
            'Gender',
        ]

class AdminForm (forms.Form):
    First_Name = forms.CharField(max_length=32, required=True)
    Last_Name = forms.CharField(max_length=32, required=True)

    class Meta:
        fields = [
            'First_Name',
            'Last_Name'
        ]

class UserForm (forms.Form):
    Email = forms.EmailField(required=True)
    Password = forms.CharField(max_length=32, min_length=8, widget=forms.PasswordInput)
    Password_Confirm = forms.CharField(max_length=32, min_length=8, widget=forms.PasswordInput)

    class Meta:
        fields = [
            'Email',
            'Password',
            'Password_Confirm'
        ]

    def clean_Password(self):
        password = self.cleaned_data.get("Password")
        password2 = self.cleaned_data.get("Password_Confirm")
        if (password != password2):
            raise forms.ValidationError('Passwords do not match')
        return password

