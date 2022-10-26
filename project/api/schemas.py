from ninja import ModelSchema 

from account_management.models import Account 


class AccountSchema(ModelSchema): 
    class Config:
        model = Account 
        model_fields = ['number', 'description', 'debit_account']

class AccountResponseSchema(ModelSchema): 
    class Config:
        model = Account 
        model_fields = ['id', 'number', 'description', 'debit_account']

