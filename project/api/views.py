import traceback
import datetime 
import pytz

from ninja import NinjaAPI 
from ninja.errors import AuthenticationError 

from django.contrib.auth import authenticate, login, get_user_model
from django.conf import settings

from .schemas import UserSchema, UserResponseSchema
# Create your views here.

api = NinjaAPI(version="1", csrf=True)


@api.post('/login', response=UserResponseSchema) 
def login_user(request, data: UserSchema):
    if not get_user_model().objects.filter(username=data.username).exists():
        raise AuthenticationError()
    user = authenticate(request, username=data.username, password=data.password)
    if user is not None: 
        login(request, user)
        user.last_login = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)) 
        user.save()
        return user
    else: 
        raise AuthenticationError() 

@api.exception_handler(AuthenticationError)
def authentication_error(request, exc): 
    return api.create_response(request, {
        "message": "Invalid credentials"
    }, status=401)

@api.exception_handler(Exception) 
def server_error(request, exc): 
    return api.create_response(request, {
        "message": traceback.format_exception(exc) if settings.DEBUG else "Internal server error"  
    }, status=500)