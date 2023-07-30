from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf.urls.static import static
from .form import *
from .models import *

from django.contrib.auth.models import User, Group


from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
def home(request):
    user = request.user
    is_logged_in = False

    if user == None:
        is_logged_in = False
    else:
        is_logged_in = True

    context = {'is_logged_in': is_logged_in}

    return render(request, 'index.html', context)

def register(request):
    register_form = RegisterForm()

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)    

        if register_form.is_valid():
            user = register_form.save()

            username = register_form.cleaned_data.get('username')
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            Customer.objects.create(user = user, name = username)
            return redirect('home')

        else:
            print(register_form.error_messages)

    context = {"form" : register_form}
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        group = None

        is_admin = False

        user = authenticate(request, username=username, password = password)
        if user is not None:
            auth_login(request, user)

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

                if group == 'admin':
                    is_admin = True

            
            context = {"is_admin": is_admin}

            return render(request,'index.html', context)
        else:
            messages.info(request, "Username or Password incorrect")

    return render(request, 'login.html')

def customer(request, name):
    user = User.objects.get(username = name)
    customer = Customer.objects.get(user=user)

    context = {'customer' : customer}

    return render(request, 'customer.html', context)

def logout(request):
    auth_logout(request)

    return redirect('home')
    
