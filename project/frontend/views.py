from django.shortcuts import render
from django.urls import reverse

from .forms import AuthenticationForm


# Create your views here.
def account_management(request, user_id): 
    return render(request, 'frontend/account_management.html')

def login_page(request): 
    form = AuthenticationForm()
    login_api_endpoint = reverse('api-1:login_user')
    return render(request, 'frontend/login_page.html', context={
        'form': form, 
        'post_url': login_api_endpoint
    })