from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from homepage.forms import *
from employee_page.models import *
from django.contrib.auth.models import User
# Create your views here.

def index(request): 
        
    return render(request, 'homepage.html')


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:

            attempt = request.session["attempt"] or 0
            request.session["attempt"] = attempt + 1
            return render(request, "login.html", {"form": form, "invalid_user": True})

        else:
             
            login(request, user)
                
            first_name = request.user.first_name
            last_name = request.user.last_name
     
            employee_record = Employees.objects.get(first_name=first_name, last_name=last_name)
            
            print(employee_record.emp_no)
            
            variables = { 'current_page': 'homepage', 'employee_record': employee_record }

            return render(request, 'homepage.html', variables)
            
    return render(request, "login.html", {"form": form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage:index'))

def keycloak(request):
    return HttpResponseRedirect(reverse('homepage:index'))