from django.db import models
from django.contrib.auth.models import User


# We create this model(class) to add additional information for the User that the default-user doesn't have
class UserProfileInfo(models.Model):

    #Default user alreday have (Name, pass, email etc.). To add extra attribute we need to use "OneToOneField"() relationship
    user = models.OneToOneField(User, on_delete=models.CASCADE) #This parameter(on_delete=models.CASCADE) is snew in update vertion of django

    #Here are the additional attributes we want
    portfolio_site = models.URLField(blank=True)
    #User can add a URL of their portfolio (if they have). And (blank=True, means it is not mandatory). There will not be an error if they dont provide


    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    #Because we use upload to (which means to a place)"profile_pics", we must create a folder with same name under 'media'


    def __str__(self):
        return self.user.username
        #Here 'username' is the attribute of default 'User'(that we import at the top)
