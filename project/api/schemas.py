from ninja import ModelSchema 

from account_management.models import Account 


class AccountSchema(ModelSchema): 
    class Config:
        model = Account 
        model_fields = ['number', 'name', 'description', 'notes', 'debit_account']

class AccountResponseSchema(ModelSchema): 
    class Config:
        model = Account 
        model_fields = ['id', 'number', 'name', 'description', 'notes', 
                        'debit_account']

