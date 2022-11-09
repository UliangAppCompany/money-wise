import datetime 
import pytz

from django.contrib.auth import get_user_model, authenticate, login
from django.conf import settings
from ninja import Router

from ..schemas import UserSchema, UserResponseSchema
from ..exceptions import ApiAuthError

router = Router()

@router.post('/login', response=UserResponseSchema) 
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
