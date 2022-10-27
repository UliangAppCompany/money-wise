import datetime 
import pytz
from ninja import NinjaAPI 
from ninja.security import django_auth

from django.contrib.auth import authenticate, login
from django.conf import settings

from account_management.models import Ledger, Account

from .schemas import AccountSchema, AccountResponseSchema
from .schemas import UserSchema, UserResponseSchema
from .exceptions import InvalidCredentialsError
# Create your views here.

api = NinjaAPI(version='1', csrf=True)

@api.post("/ledger/{ledger_id}/account", response = {
    200: AccountResponseSchema }, auth=django_auth)
def add_new_account(request, ledger_id:int, data:AccountSchema): 
    ledger = Ledger.objects.get(id=ledger_id) 
    account = Account.objects.create(ledger=ledger, **data.dict())
    ledger.save()
    return 200, account
    
@api.post('/login', response=UserResponseSchema) 
def login_user(request, data: UserSchema):
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None: 
        login(request, user)
        user.last_login = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)) 
        user.save()
        return user
    else: 
        raise InvalidCredentialsError() 

