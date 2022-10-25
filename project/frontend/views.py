import re
from typing import List
from django.shortcuts import render
from django.contrib.auth import get_user
from django.urls import reverse_lazy

from .forms import AccountManagementAddAccountForm

# Create your views here.
def add_account(request, ledger_id): 
    add_account_form =  AccountManagementAddAccountForm()
    user = get_user(request)
    ledger = user.ledgers.get(id=ledger_id)
    add_account_url = reverse_lazy("api-1:add-new-account")
    return render(request, 'frontend/add_account_page.html',
       context={
            'form': add_account_form, 
            'ledger':ledger,  
            'post_url': add_account_url}
        )

def list_accounts(request): 
    ...