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

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user", "set_up_validated_user")
def test_add_account_page_loads(client): 
    client.login(username='john@example.com', password='password')
    response = client.get('/ledger/1/account')

    assert response.status_code == 200 

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user", "set_up_validated_user")
def test_template_renders_with_correct_context(client): 

    client.login(username='john@example.com', password='password')
    response = client.get('/ledger/1/account') 
    context = response.context 

    assert isinstance(context['add_account_form'], AccountManagementAddAccountForm)  
    assert isinstance(context['ledger'], Ledger)
    assert 'frontend/account_management.html' in [template.name for template in response.templates]