from django.contrib.auth import login as auth_login, authenticate
from django.shortcuts import render
from excurtionManager.models import Client, Product, Excurtion, Notification
from tursoft.forms import UserForm
from excurtionManager.forms import ExcurtionForm
import datetime

def home(request):
    if not request.user.is_anonymous():
        return render(
                  request,
                  'dashboard.html',
                  {
                  'products':Product.objects.filter(excurtion__date_from__lte=datetime.datetime.today())[:10],
                  'clients':Client.objects.all()[:10],
                  'excurtions':Excurtion.objects.all()[:10],
                  'notifications':Notification.objects.all()[:10],
                  'form_excurtion': ExcurtionForm(),
                   }
              )
    else:
        return render(
              request,
              'login.html',
              {}
          )
    
def login(request):
    user = authenticate(username=request.POST['user'], password=request.POST['pass'])
    
    if user is not None:
            auth_login(request,user)
       
    return home(request)
    
def register(request):
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES)
        
        if user_form.is_valid():
            u = user_form.save()
                    
        return render(
                  request,
                  'dashboard.html',
                  {}
              )
    user_form = UserForm()
        
    return render(
              request,
              'register.html',
              {
               'form':user_form
               }
          )