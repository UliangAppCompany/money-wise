from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model 

from .service import validate_user
# Create your views here.

def validate_registration(request): 
    token = request.GET['token'] 
    username = request.GET['username']
    user  = get_object_or_404(get_user_model(), username=username)
    # breakpoint()
    if user.token_is_valid(token): 
        validate_user(user)
    return HttpResponseRedirect(reverse('set-new-password',args= [ user.id ])) 


def set_new_password(request, user_id): 
    ...
