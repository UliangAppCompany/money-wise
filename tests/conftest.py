import os 
from datetime import datetime

import pytest 

from django.db import connection 
from django.test import Client 

from account_management.models import Journal, Ledger, Transaction
from registration.service import create_user, get_user 

os.environ["NINJA_SKIP_REGISTRY"] = "yes"

@pytest.fixture 
def john(): 
    user = create_user('john@example.com')
    return user

@pytest.fixture 
def cursor(): 
    cursor_ = connection.cursor() 
    yield cursor_ 
    cursor_.close()

@pytest.fixture 
def journal(): 
    return Journal.objects.create(number=1, name="Company A Journal") 

@pytest.fixture 
def ledger(): 
    return Ledger.objects.create(number=1, name="Company A General Ledger")  

@pytest.fixture 
def add_accounts_to_ledger(ledger): 
    ledger.create_account(number=100, description="Cash", debit_account=True, 
        category="AS")  
    
    ledger.create_account(number=200, description="Checking", debit_account=False, 
        category="LB")

    ledger.create_account(number=300, description="Revenue", debit_account=False, 
        category="RV")
    
@pytest.fixture 
def collection_transactions(ledger): 
    cash_account = ledger.get_account(100) 
    debit_trans = Transaction(account=cash_account, debit_amount=1050, 
        description='from 300-Revenue account') 

    rev_account = ledger.get_account(300) 
    credit_trans = Transaction(account=rev_account, credit_amount=1050, 
        description='to 100-Cash account')

    Transaction.objects.bulk_create([debit_trans, credit_trans])
    return debit_trans, credit_trans

@pytest.fixture 
def collect_from_cash_register(journal, collection_transactions): 
    now = datetime.utcnow()
    journal.create_double_entry(date=now, 
        note="being collections from cash register", 
        transactions=collection_transactions)

@pytest.fixture 
def create_current_account(ledger): 
    account = ledger.create_account(number=100, description="Current Assets", category="AS")
    account.is_control = True 
    account.save()

@pytest.fixture 
def create_cash_accounts(ledger):
    acc101 = ledger.create_account(number=101, description="Cash in Bank 1", category="AS") 
    acc102 = ledger.create_account(number=102, description="Cash in Bank 2", category="AS") 
    

@pytest.fixture 
def categorize_accounts(ledger): 
    cash = ledger.get_account(100)
    cash.add_subaccounts(*[ledger.get_account(n) for n in (101, 102)])
    cash.save()
    
@pytest.fixture 
def client(): 
    client_ = Client() 
    return client_ 

@pytest.fixture 
def john_adds_ledger(ledger): 
    john = get_user('john@example.com')
    john.ledgers.add(ledger)
    john.save() 

@pytest.fixture 
def john_adds_journal(journal): 
    john = get_user('john@example.com')
    john.journals.add(journal) 
    john.save()
    
@pytest.fixture 
def login_john(client):
    client.login(username="john@example.com", password="password")

@pytest.fixture
def init_john(): 
    create_user('john@example.com', password='password', require_validation=False)