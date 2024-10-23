from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
import requests




# Registration Form

def register(request):
    form = UserCreationForm()
    return render(request, 'register.html', {'form': form})