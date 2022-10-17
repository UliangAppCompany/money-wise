from datetime import datetime, timezone
import pytest 



@pytest.mark.django_db 
def test_init_journal(cursor, journal): 

    result = cursor.execute("select number, name from account_management_journal") \
        .fetchall()

    assert result == [(1, 'Company A Journal')]

@pytest.mark.django_db
def test_init_ledger(cursor, ledger): 
    
    result = cursor.execute("select number, name from account_management_ledger") \
        .fetchall() 

    assert result == [(1, "Company A General Ledger")] 

@pytest.mark.django_db 
@pytest.mark.usefixtures("add_accounts_to_ledger")
def test_ledger_create_account(cursor, ledger): 
    
    result = cursor.execute(
        "select number, description, debit_account, category " 
        "from account_management_account "
        "where ledger_id = %s", [ledger.id]).fetchall() 

    assert len(result) ==2  
    assert set(result) == {
        (100, "Cash", True, "AS"), 
        (200, "Checking", False, "LB")
    }

@pytest.mark.django_db 
@pytest.mark.usefixtures("add_accounts_to_ledger")
def test_get_account_from_ledger(ledger): 
    cash_account = ledger.get_account(number=100)
    
    assert cash_account.description == "Cash"

@pytest.mark.django_db 
@pytest.mark.usefixtures("add_accounts_to_ledger")
def test_account_create_balance_entry(cursor, ledger): 
    cash_account = ledger.get_account(number=100) 
    fmt = '%Y-%m-%d %H:%M:%S'
    tz = timezone.utc
    cash_account.create_balance(debit_amount=1050, 
        description="being collections from cash register", 
        date=datetime.strptime("2022-10-16 16:00:00", fmt).replace(tzinfo=tz)) 

    result = cursor.execute(
        "select debit_amount, credit_amount, debit_balance, description " 
        "from account_management_balance "
        "where account_id = %s", [cash_account.id]).fetchall()

    assert result == [(1050, 0, 1050, "being collections from cash register")]
    
    cash_account.create_balance(credit_amount=950, 
        description="being payment of invoice-XXX", 
        date=datetime.strptime("2022-10-17 15:30:00", fmt).replace(tzinfo=tz)) 

    result = cursor.execute(
        "select debit_amount, credit_amount, debit_balance, description " 
        "from account_management_balance "
        "where account_id = %s"
        "order by date desc", [cash_account.id]).fetchall()

    assert result == [
        (0, 950, 100, "being payment of invoice-XXX"), 
        (1050, 0, 1050, "being collections from cash register")
    ]

@pytest.mark.django_db 
def test_journal_create_entry(cursor, journal): 
    now = datetime.utcnow()
    journal.create_entry(date=now, notes="Being payment of invoice-XXX")
    
    result = cursor.execute("select notes " 
            "from account_management_entry " 
            "where journal_id == %s", [journal.id]).fetchall() 

    assert result == [('Being payment of invoice-XXX',)] 

