from django.urls import path
from basic_app import views


#This is for RELATIVE-TEMPLATE-TAGGING
#It is going to look under the template tag and find the URLS that matches
app_name = 'basic_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    # This both path coming from templates under a basic_app folder and already connected to our main URLS page
]
