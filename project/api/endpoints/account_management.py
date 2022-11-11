from ninja import  Router
from ninja.security import django_auth

from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404

from ..schemas import LedgerSchema, LedgerResponseSchema
from ..schemas import AccountSchema, AccountResponseSchema
from ..schemas import JournalSchema, JournalResponseSchema
from ..schemas import CategorizeAccountResponseSchema, CategorizeAccountSchema
from account_management.models import Ledger, Account, Journal


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
    
@router.post('/journal', auth=django_auth, response=JournalResponseSchema )
def add_journal(request, data: JournalSchema): 
    user = get_user(request)
    journal = Journal.objects.create(**dict(data)) 
    user.journals.add(journal)
    user.save()
    return journal

@router.put('/ledger/{ledger_id}/account/{account_id}', 
    response=CategorizeAccountResponseSchema, 
    auth=django_auth)
def categorize_account(request, ledger_id:int, account_id:int, data: CategorizeAccountSchema):
    ledger = get_object_or_404(Ledger, id=ledger_id)
    control_account = get_object_or_404(Account, id=account_id)
    control_account.add_subaccounts(*[
        Account.objects.get_or_create(ledger=ledger, **dict(obj))[0] for obj in data.subaccounts
    ])
    return control_account