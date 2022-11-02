import traceback
import datetime 
import pytz

from ninja import NinjaAPI 
from ninja.errors import AuthenticationError 
from ninja.security import django_auth

from django.contrib.auth import authenticate, login, get_user_model, get_user
from django.conf import settings

from account_management.models import Ledger, Account

from .schemas import AccountSchema, AccountResponseSchema
from .schemas import UserSchema, UserResponseSchema
from .schemas import LedgerSchema, LedgerResponseSchema
# Create your views here.

api = NinjaAPI(version="1", csrf=True)

class ApiAuthError(AuthenticationError): 
    def __init__(self, message, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.message = message

    def __str__(self): 
        return self.message

@api.post('/ledger', auth=django_auth, response=LedgerResponseSchema) 
def add_ledger(request, data: LedgerSchema): 
    user = get_user(request) 
    ledger = Ledger.objects.create(**dict(data))
    user.ledgers.add(ledger)
    user.save()
    return ledger

@api.post("/ledger/{ledger_id}/account", response = AccountResponseSchema,  
     auth=django_auth)
def add_account(request, ledger_id:int, data:AccountSchema): 
    ledger = Ledger.objects.get(id=ledger_id) 
    account = Account.objects.create(ledger=ledger, **dict(data))
    ledger.save()
    return account
    
@api.post('/login', response=UserResponseSchema) 
def login_user(request, data: UserSchema):
    if not get_user_model().objects.filter(username=data.username).exists():
        raise ApiAuthError(f"User with username {data.username} not found")
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None: 
        login(request, user)
        user.last_login = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)) 
        user.save()
        return user
    else: 
        raise ApiAuthError("Invalid credentials.") 

@api.exception_handler(AuthenticationError)
def authentication_error(request, exc): 
    return api.create_response(request, {
        "message": str(exc),  
        "tb": traceback.format_exception(exc) if settings.DEBUG else ""
    }, status=401)

@api.exception_handler(Exception) 
def server_error(request, exc): 
    return api.create_response(request, {
        "message": str(exc), 
        "tb": traceback.format_exception(exc) if settings.DEBUG else ""  
    }, status=500)