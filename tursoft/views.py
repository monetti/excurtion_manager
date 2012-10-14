from django.contrib.auth import login, authenticate
from django.shortcuts import render
from excurtionManager.models import Client, Product, Excurtion, Notification
from tursoft.forms import UserForm
import datetime


def home(request):
    if request.user:
        return render(
                  request,
                  'dashboard.html',
                  {
                  'products':Product.objects.filter(excurtion__date_from__lte=datetime.datetime.today())[:10],
                  'clients':Client.objects.all()[:10],
                  'excurtions':Excurtion.objects.all()[:10],
                  'notifications':Notification.objects.all()[:10],
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
        if user.is_active:
            login(request, user)
            return render(
                      request,
                      'dashboard.html',
                      {}
                  )
        else:
            print("Your account has been disabled!")
    else:
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
    
        