from datetime import datetime
import pytest 
from django.db import connection 
from django.test import Client 


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

    ledger.create_account(number=300, description="Revenue", debit_account=False, 
        category="RV")
    

@pytest.fixture 
def collect_from_cash_register(ledger, journal): 
    now = datetime.utcnow()
    journal.create_double_entry(ledger, date=now, notes="being collections from cash register", 
            transactions = {
                300: {'credit_amount': 1050, 'debit_amount': 0}, 
                100: {'credit_amount': 0, 'debit_amount': 1050}
            })

@pytest.fixture 
def create_cash_accounts(ledger):
    ledger.create_account(number=101, description="Cash in Bank 1", category="AS") 
    ledger.create_account(number=102, description="Cash in Bank 2", category="AS") 

@pytest.fixture 
def client(): 
    client_ = Client() 
    return client_ 