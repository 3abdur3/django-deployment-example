from django import forms
from django.contrib.auth.models import User #This "User" is defauilt django's model
from basic_app.models import  UserProfileInfo #We created 'UserProfileInfo' in model.py

#We gonna use here two forms

#This is the base form (original)
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    #We want to edit the password a bit as we have mentioned in the setting that we want users to put at least "8 Characters"

    #This meta(class) provides info that connecting the 'model' to the 'Form'
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

#This is for the additional attributes in the form
class UserProfileInfoForm(forms.ModelForm): #We inherarte from "froms.ModelForm"
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
