import pytest 
from django.db import connection 

from account_management.models import Journal, Ledger


@pytest.fixture 
def cursor(): 
    cursor_ = connection.cursor() 
    yield cursor_ 
    cursor_.close()


@pytest.fixture 
def journal(): 
    journal_ = Journal(number=1, name="Company A Journal") 
    journal_.save()
    return journal_

@pytest.fixture 
def ledger(): 
    ledger_ = Ledger(number=1, name="Company A General Ledger")  
    ledger_.save() 

    return ledger_ 

@pytest.fixture 
def add_accounts_to_ledger(ledger): 
    ledger.create_account(number=100, description="Cash", debit_account=True, 
        category="AS")  
    
    ledger.create_account(number=200, description="Checking", debit_account=False, 
        category="LB")
    
