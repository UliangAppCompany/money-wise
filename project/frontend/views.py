import re
from typing import List
from django.shortcuts import render
from django.contrib.auth import get_user
from django.urls import reverse

from .forms import AccountManagementAddAccountForm

# Create your views here.
def add_account(request, ledger_id): 
    add_account_form =  AccountManagementAddAccountForm()
    user = get_user(request)
    ledger = user.ledgers.get(id=ledger_id)
    add_account_url = reverse("api-1:add-new-account")
    ledger_page = reverse("ledger-page", args=[ledger_id])
    return render(request, 'frontend/add_account_page.html',
       context={
            'form': add_account_form, 
            'ledger':ledger,  
            'post_url': add_account_url, 
            'ledger_page': ledger_page}
        )

def ledger_management(request, ledger_id): 
    if request.method == "POST": 
        # [TODO]: do post 
        pass        
    elif request.method == "GET": 
        # [TODO]: return a list of accounts in ledger. 
        pass