import datetime 
import pytz
from ninja import NinjaAPI 
from ninja.security import django_auth

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.conf import settings

from .schemas import UserSchema, UserResponseSchema
from .exceptions import InvalidCredentialsError
# Create your views here.

api = NinjaAPI(csrf=True)


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

