from django.contrib.auth.models import User
from django.forms import models

class UserForm(models.ModelForm):
    
    class Meta:
       model = User 
        

