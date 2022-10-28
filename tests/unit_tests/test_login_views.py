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


def test_login_route(login_response): 
    assert login_response.status_code == 200 

def test_user_can_login_to_the_application(client): 
    client.post('/api/login', data={'username': 'john@example.com', 
        'password': 'password'},  
        content_type = 'application/json')

    factory = RequestFactory() 
    request = factory.get('/') 
    request.session = client.session 

    user = get_user(request)
    assert user.username == 'john@example.com' 

def test_login_page_loads(client): 
    response = client.get('/login') 

    assert response.status_code == 200 
