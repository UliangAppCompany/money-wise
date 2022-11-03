from django.shortcuts import render
from django.contrib.auth import get_user
from django.urls import reverse

from account_management.models import Ledger 

from .forms import AccountManagementAddAccountForm, AuthenticationForm, ChangePasswordForm

# Create your views here.
def add_account(request, ledger_id): 
    add_account_form =  AccountManagementAddAccountForm()
    user = get_user(request)
    ledger = user.ledgers.get(id=ledger_id)
    add_account_url = reverse("api-1:add_account", kwargs={'ledger_id': 
        ledger_id})
    ledger_page = reverse("ledger-page", args=[ledger_id])
    return render(request, 'frontend/add_account_page.html',
       context={
            'form': add_account_form, 
            'ledger':ledger,  
            'post_url': add_account_url, 
            'ledger_page': ledger_page}
        )

def ledger_page(request, ledger_id): 
    items = Ledger.objects.get(id=ledger_id).accounts.all()
    # [TODO]: pass on to ledger page

def login_page(request): 
    form = AuthenticationForm()
    login_api_endpoint = reverse('api-1:login_user')
    return render(request, 'frontend/login_page.html', context={
        'form': form, 
        'post_url': login_api_endpoint
    })

def change_password_page(request, user_id): 
    return render(request, 'frontend/reset_password.html', context={
        'form': ChangePasswordForm(), 
        'post_url': reverse('api-1:patch_user', args=[user_id]), 
    })