from django.shortcuts import render
from django.contrib.auth import get_user

from .forms import AccountManagementAddAccountForm

# Create your views here.
def account_management(request, ledger_id): 
    add_account_form =  AccountManagementAddAccountForm()
    user = get_user(request)
    ledger = user.ledgers.get(id=ledger_id)
    return render(request, 'frontend/account_management.html',
        )
