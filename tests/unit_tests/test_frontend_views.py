import pytest

from django.contrib.auth import get_user_model

from frontend.forms import AccountManagementAddAccountForm 
from account_management.models import Ledger


@pytest.fixture 
def set_up_validated_user(ledger): 
    user = get_user_model().objects.get(username='john@example.com')
    user.is_validated=True
    user.set_password('password') 
    user.ledgers.add(ledger)
    user.save() 

@pytest.fixture 
def login(client): 
    client.login(username='john@example.com', password='password')

@pytest.fixture 
def response(client): 
    response_ = client.post('/api/ledger/1/account',
        data={'number': 101, 'description': 'Bank A Account', 'debit_account': True },
        content_type='application/json')
    return response_

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user", "set_up_validated_user", 
                        "login")
def test_add_account_page_loads(client): 
    response = client.get('/ledger/1/account')

    assert response.status_code == 200 

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user", "set_up_validated_user", 
            "login")
def test_template_renders_with_correct_context(client): 
    response = client.get('/ledger/1/account') 
    context = response.context 

    assert isinstance(context['form'], AccountManagementAddAccountForm)  
    assert isinstance(context['ledger'], Ledger)
    assert 'frontend/add_account_page.html' in [template.name for template in response.templates]

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user", "set_up_validated_user", "login")
def test_can_post_to_ledger_page(response): 
    assert response.status_code == 200

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user", "set_up_validated_user", 
                        "login", "response") 
def test_post_to_ledger_page_updates_db(cursor):
    result = cursor.execute("select number, description, debit_account from " 
        "account_management_account "
        "where number = 101 and " 
        "ledger_id = 1").fetchone() 

    assert result == (101, 'Bank A Account', True)  

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user", "set_up_validated_user") 
def test_that_cannot_make_unauthenticated_api_calls(response): 
    assert response.status_code == 401