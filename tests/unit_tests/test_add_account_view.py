import pytest


pytestmark = [
    pytest.mark.django_db, 
    pytest.mark.usefixtures("register_new_user", "validate_new_user", 
        "user_creates_ledger", "login_user")]

@pytest.fixture
def post_response(client, ledger): 
    response = client.post(f'/api/ledger/{ledger.id}/account', data={
        'number': 100, 
        'name': 'Cash', 
        "description": "Description", 
        "notes": "Cash on hand.", 
        'category': "AS", 
        'is_control': False, 
        "debit_account": True}, 
        
    content_type="application/json")  
    
    return response


def test_add_account_view_returns_ok_status(post_response): 
    assert post_response.status_code == 200 

def test_add_account_view_returns_proper_parsed_object(post_response): 
    parsed_object = post_response.json() 

    assert  { 'id', 'name', 'number', 'description', 'notes', 'is_control', 
    'category', 'debit_account', 'created_on', 'updated_on', 'ledger', 'control' } ==set(parsed_object.keys())

def test_add_account_view_adds_resource_to_db(post_response, cursor): 
    cursor.execute("select * from account_management_account "
    " join account_management_ledger on account_management_account.ledger_id = account_management_ledger.id " 
    " where account_management_account.number = 100 "
    " and account_management_ledger.user_id = (select id from registration_user " 
    " where username = 'john@example.com')")

    result = cursor.fetchall()
    assert len(result) != 0 
    
