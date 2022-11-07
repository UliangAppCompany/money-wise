import pytest

from django.contrib.auth import get_user_model

from frontend.forms import AccountManagementAddAccountForm 
from account_management.models import Ledger

pytestmark = [
    pytest.mark.django_db, 
    pytest.mark.usefixtures("register_new_user", "validate_new_user", 
        "user_creates_ledger")
]

@pytest.fixture 
def post_response(client, ledger): 
    client.login(username='john@example.com', password='password')
    response_ = client.post(f'/api/ledger/{ledger.id}/account',
        data={'number': 101, 'description': 'Bank A Account', 'debit_account': True },
        content_type='application/json')
    return response_

@pytest.fixture 
def get_response(client, ledger): 
    client.login(username='john@example.com', password='password')
    response = client.get(f'/ledger/{ledger.id}/account')
    return response 


def test_add_account_page_loads(get_response): 
    assert get_response.status_code == 200 

def test_template_renders_with_correct_context(get_response): 
    context = get_response.context 

    assert isinstance(context['form'], AccountManagementAddAccountForm)  
    assert isinstance(context['ledger'], Ledger)
    assert 'account_management/add_account_page.html' in [template.name for template in get_response.templates]

def test_can_post_to_api_endpoint_and_update_db(post_response, cursor, ledger): 
    assert post_response.status_code == 200

    cursor.execute("select number, description, debit_account from " 
        "account_management_account "
        "where number = 101 and " 
        "ledger_id = %s ", [ledger.id]) 

    result = cursor.fetchone()
    assert result == (101, 'Bank A Account', True)  

def test_that_cannot_make_unauthenticated_api_calls(client): 
    response_ = client.post('/api/ledger/1/account',
        data={'number': 101, 'description': 'Bank A Account', 'debit_account': True },
        content_type='application/json')
    assert response_.status_code == 401