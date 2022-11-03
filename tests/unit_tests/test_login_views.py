import pytest 

from django.contrib.auth import get_user
from django.test import RequestFactory

pytestmark =  [
    pytest.mark.django_db,
    pytest.mark.usefixtures(
        "register_new_user", 
        "validate_new_user"
    )]

@pytest.fixture 
def login_response(client): 
    response = client.post('/api/login', data={'username': 'john@example.com', 
        'password': 'password'},  
        content_type = 'application/json')
    return response


def test_login_route(login_response, client): 
    assert login_response.status_code == 200 

    factory = RequestFactory() 
    request = factory.get('/') 
    request.session = client.session 

    user = get_user(request)
    assert user.username == 'john@example.com' 

def test_login_page_loads(client): 
    response = client.get('/login') 

    assert response.status_code == 200 

def test_change_password_page_loads(client): 
    response = client.get('/user/1/change-password')

    assert response.status_code == 200
