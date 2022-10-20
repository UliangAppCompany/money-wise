from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def validate_registration(request): 
   return HttpResponseRedirect(reverse('set-new-password')) 


def set_new_password(request): 
    ...
