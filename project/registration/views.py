from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model 

# Create your views here.

def validate_registration(request): 
    token = request.GET['token'] 
    username = request.GET['username']
    user = get_user_model().objects.get(username=username) 
    # breakpoint()
    if user.token_is_valid(token): 
        user.is_validated = True
        user.save() 

    return HttpResponseRedirect(reverse('set-new-password')) 


def set_new_password(request): 
    ...
