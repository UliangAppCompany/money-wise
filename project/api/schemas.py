from ninja import ModelSchema, Schema

from django.contrib.auth import get_user_model

from account_management.models import Account,Ledger


class UserSchema(Schema): 
    username: str 
    password: str


class UserResponseSchema(ModelSchema): 
    class Config: 
        model = get_user_model() 
        model_exclude = ['password', 'validation_token']

class LedgerSchema(ModelSchema): 
    class Config: 
        model = Ledger 
        model_fields = ['number', 'name', 'description'] 


class LedgerResponseSchema(ModelSchema): 
    class Config: 
        model = Ledger 
        model_exclude = ['user']
    
class AccountSchema(ModelSchema): 
    class Config:
        model = Account 
        model_exclude = ['control', 'id', 'ledger', 'created_on', 'updated_on']

class AccountResponseSchema(ModelSchema): 
    class Config:
        model = Account 
        model_fields = '__all__'

