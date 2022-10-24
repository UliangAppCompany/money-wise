from django.shortcuts import render
from django.contrib.auth import get_user
from django.urls import reverse_lazy
from django.contrib.auth.models import AnonymousUser

from .forms import AccountManagementAddAccountForm

# Create your views here.
def add_new_account(request, ledger_id): 
    add_account_form =  AccountManagementAddAccountForm()
    user = get_user(request)
    ledger = None
    if not isinstance(user, AnonymousUser): 
        ledger = user.ledgers.get(id=ledger_id)
    add_account_url = reverse_lazy("api-1:add-new-account")
    return render(request, 'frontend/add_new_account.html',
       context={
            'form': add_account_form, 
            'ledger':ledger,  
            'post_url': add_account_url}
        )

def list_accounts(request): 
    ...