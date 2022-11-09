from ninja import  Router
from ninja.security import django_auth

from django.contrib.auth import get_user

from ..schemas import LedgerSchema, LedgerResponseSchema
from ..schemas import AccountSchema, AccountResponseSchema
from account_management.models import Ledger, Account


router = Router()

@router.post('/ledger', auth=django_auth, response=LedgerResponseSchema) 
def add_ledger(request, data: LedgerSchema): 
    user = get_user(request) 
    ledger = Ledger.objects.create(**dict(data))
    user.ledgers.add(ledger)
    user.save()
    return ledger

@router.post("/ledger/{ledger_id}/account", response = AccountResponseSchema,  
     auth=django_auth)
def add_account(request, ledger_id:int, data:AccountSchema): 
    ledger = Ledger.objects.get(id=ledger_id) 
    account = Account.objects.create(ledger=ledger, **dict(data))
    ledger.save()
    return account
    