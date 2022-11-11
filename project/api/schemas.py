from ninja import ModelSchema, Schema

from django.contrib.auth import get_user_model

from account_management.models import Account,Ledger, Journal


class JournalSchema(ModelSchema): 
    class Config: 
        model = Journal 
        model_fields = ['number', 'name', 'description']

class JournalResponseSchema(ModelSchema): 
    class Config: 
        model = Journal 
        model_exclude = ['user']

class UserSchema(Schema): 
    username: str 
    password: str

class UserSetPasswordSchema(Schema): 
    password: str 
    retype_password:str

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

class CategorizeAccountSchema(ModelSchema): 
    class Config:
        model = Account 
        model_exclude = ['control', 'ledger', 'created_on', 'updated_on']
    subaccounts: list[AccountSchema]
    
class AccountResponseSchema(ModelSchema): 
    class Config:
        model = Account 
        model_fields = '__all__'

class CategorizeAccountResponseSchema(ModelSchema): 
    class Config:
        model = Account 
        model_exclude = ['control']
    subaccounts: list[AccountResponseSchema]
