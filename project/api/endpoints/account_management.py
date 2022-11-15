from traceback import format_exception 
from ninja import  Router
from ninja.security import django_auth

from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404
from django.conf import settings

from ..schemas import LedgerSchema, LedgerResponseSchema
from ..schemas import AccountSchema, AccountResponseSchema
from ..schemas import JournalSchema, JournalResponseSchema
from ..schemas import CategorizeAccountResponseSchema, CategorizeAccountSchema
from ..schemas import EntrySchema, EntryResponseSchema
from ..schemas import Errors

from account_management.models import Ledger, Account, Journal, Transaction
from account_management.exceptions import DoubleEntryError


router = Router()

@router.post('/ledger', auth=django_auth, response=LedgerResponseSchema) 
def add_ledger(request, data: LedgerSchema): 
    user = get_user(request) 
    ledger = Ledger.objects.create(**dict(data))
    user.ledgers.add(ledger)
    user.save()
    return ledger

@router.get('/ledger/{ledger_id}/account', response = list[AccountResponseSchema]) 
def list_accounts(request, ledger_id:int, category:int = 0):  
    ledger =Ledger.objects.get(id=ledger_id) 

    results = ledger.get_account(category).subaccounts.all() \
        if category else Account.objects.filter(ledger=ledger, is_control=False).all()

    return results

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

@router.post('/journal/{journal_id}/entry', response={200: EntryResponseSchema, 
    400: Errors},  auth=django_auth)
def add_entry(request, journal_id:int, data:EntrySchema): 
    journal = Journal.objects.get(id=journal_id) 
    user = get_user(request) 
    transactions = [] 
    for transaction in data.transactions:
        account = Account.objects.filter(ledger__user = user, number=transaction.number).get()
        transactions.append(
            Transaction.objects.create(account=account, 
                debit_amount=transaction.debit_amount, 
                credit_amount=transaction.credit_amount, 
                description=transaction.description) 
        )          
    try: 
        entry = journal.create_double_entry(date=data.date, note=data.note, 
            transactions=transactions )
        journal.save() 
    except DoubleEntryError as exc: 
        tb = format_exception(exc) if settings.DEBUG else [] 
        return 400, Errors(message=str(exc), tb=tb) 
    return 200, entry

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

