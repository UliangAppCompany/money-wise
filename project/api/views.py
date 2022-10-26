from ninja import NinjaAPI 
from ninja.security import django_auth

from account_management.models import Ledger, Account

from .schemas import AccountSchema, AccountResponseSchema
# Create your views here.

api = NinjaAPI(version='1', csrf=True)

@api.post("/ledger/{ledger_id}/account", response = {
    200: AccountResponseSchema }, auth=django_auth)
def add_new_account(request, ledger_id:int, data:AccountSchema): 
    ledger = Ledger.objects.get(id=ledger_id) 
    account = Account.objects.create(ledger=ledger, **data.dict())
    ledger.save()
    return 200, account
