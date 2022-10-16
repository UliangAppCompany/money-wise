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


    