from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse # This line is different in old version (from django.core.urlsolver import reverse)
from django.contrib.auth.decorators import login_required # This built-in decorater force the user to be logged in. django has a bunch of 'auth_decorators' that helps a lot



# For the basic page
def index(request):
    return render(request, 'basic_app/index.html')

# We creat a view with a special MESSAGE to the users and to make it active we must use DECORATOR
@login_required
def special(request):
    return HttpResponse("You are logged in! Thanks")

# We create this LOGOUT view. And the decorator make the log-out(function) active, only when someone LOGGED-IN
@login_required
def user_logout(request):
    logout(request) # That automatic log-out the users
    return HttpResponseRedirect(reverse('index'))


#For the registration page
def register(request):

    #If we keep it 'FALSE', means it is not registered yet.
    registered = False

    if request.method == "POST":
        #We get info from both of the 'FORM'
        user_form = UserForm(data=request.POST) #And this 'user_form' variable going to be as 'context_dic'
        profile_form = UserProfileInfoForm(data=request.POST)

        #Now we going to check if both 'Forms' are valid
        if user_form.is_valid() and profile_form.is_valid():

            #If so, then we grab everything from user_form
            user = user_form.save() #We save it directly to 'database'
            user.set_password(user.password) # This method goes "HASHING password" in the setting.py
            user.save() #Then it save here "HASH" password in the database

            #Then we grab everything from profile_form
            #We gonna deal with customed extra info that we asked from user ex- web-link and profile pic
            profile = profile_form.save(commit=False) #We use 'commit=FALSE' to manipulate the rerun data before saving it to 'database', otherwise it might save twice (to above 'user' once)
            profile.user = user #User means 'user_form'. This way setup the "OneToOne" relationship we used in model.py

            #Now we check if users provided 'profile-pic'
            if 'profile_pic' in request.FILES: #Because 'picture' is an actual FILE. can be also pdf,csv,resume etc
                profile.profile_pic = request.FILES['profile_pic'] # All the files of picture will be acticing like a dictionary
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    #This means there was NO-REQUEST yet or request!=POST
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    #Here will be our all three key dictionary value we gonna connect on HTML page with Templat-tag
    return render(request, 'basic_app/registration.html',
                            {'user_form':user_form, 'profile_form':profile_form,
                                'registered':registered})


# We create a new view for LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # We use here buil-in 'authentication(function)' which we import on the TOP already
        user = authenticate(username=username, password=password)

        # check if USER exist, means if the user is authenticated
        if user:
            if user.is_active: # Later we will apply 'deactivate' user if they logged in too long in the "CLONE" project
                login(request,user) # We import already built-in LOGIN
                # After log-in, user will be REDIRECTED TO somewhere (here is INDEX page)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            # Just to get these PRINT message on our CONSOLE
            print("Someone tried to login and failed") # Just to get this message on our CONSOLE
            print("Username: {} and password: {}".format(username,password)) # To catch if some malicious user tried to login
            return HttpResponse("Invalid login details supplied!")

    else:
        return render(request,'basic_app/login.html', {}) #We kept the dictionary empty, may use it for future
