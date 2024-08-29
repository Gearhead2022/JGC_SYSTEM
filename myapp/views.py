from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from myapp.models import Events, past_due, past_due_ledger

from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyodbc
from .forms import UserRegistrationForm

import requests
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'myapp/index.html')

def login_form(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                # return redirect('home')
                return redirect('index')
            
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})


def logout_form(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  
    else:
        form = UserRegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})



