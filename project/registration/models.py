import secrets
import datetime as dt
import pytz

from django.conf import settings
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager 
from django.contrib.auth.models import PermissionsMixin 
from django.conf import settings

from registration.exceptions import UnvalidatedUserError, TokenExpiredError

# Create your models here.
class UserManager(BaseUserManager): 
    def create_user(self, username, token, password=None): 
        user = self.model(username=username, validation_token=token)
        if password: 
            user.is_validated = True
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None): 
        if password is None: 
            raise ValueError("Password is required for superusers.")
        user = self.create_user(username, password)
        user.is_admin = True 
        user.save() 
        return user


class User(PermissionsMixin, AbstractBaseUser): 
    username = models.EmailField(unique=True) 
    is_validated = models.BooleanField(default=False) 
    validation_token = models.CharField(max_length=100, null=True) 
    first_name = models.CharField(max_length=100, null=True, blank=True)
    validation_token_issued = models.DateTimeField(auto_now_add=True)
    first_joined = models.DateTimeField(null=True)
    
    USERNAME_FIELD = 'username' 
    EMAIL_FIELD = 'username'
    
    objects = UserManager()

    def token_is_valid(self, token): 
        now = dt.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        if now - self.validation_token_issued>= settings.VALIDATION_TOKEN_EXPIRY: 
            raise TokenExpiredError()  
        return secrets.compare_digest(token, self.validation_token) 

    def get_full_name(self):
        return self.username 

    def get_short_name(self): 
        short_name = self.username.split('@')[0]
        return short_name

    def generate_validation_token(self, token=None): 
        if self.validation_token is None: 
            if token is None: 
                self.validation_token = secrets.token_urlsafe(32) 
            else: 
                self.validation_token = token 

            self.save() 
            return self.validation_token
    
    def set_password(self, password, require_validation=True): 
        if not self.is_validated and require_validation: 

            raise UnvalidatedUserError("Password cannot be set on unvalidated users.") 
        super().set_password(password)