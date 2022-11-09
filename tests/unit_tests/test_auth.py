import pytest 

from django.contrib.auth import get_user
from django.test import RequestFactory

from frontend.forms import AuthenticationForm
from registration.service import create_user


pytestmark =  [
    pytest.mark.django_db,
]

@pytest.fixture 
def register_john(): 
    create_user('john@example.com', password='password', require_validation=False)

@pytest.fixture 
def login_response(client): 
    response = client.post('/api/auth/login', data={'username': 'john@example.com', 
        'password': 'password'},  
        content_type = 'application/json')
    return response

@pytest.mark.usefixtures('register_john')
class TestLoginApiEndpoint: 
    def test_login_api_enpoint_authenticates_user(self,login_response): 
        assert login_response.status_code == 200 

    @pytest.mark.usefixtures('register_john', 'login_response')
    def test_subsequent_request_contain_authenticated_user_session_id(self, client): 
        factory = RequestFactory() 
        request = factory.get('/') 
        request.session = client.session 

        user = get_user(request)
        assert user.username == 'john@example.com' 

class TestLoginPage: 
    def test_login_page_loads(self,client): 
        response = client.get('/login') 
        assert response.status_code == 200 

    def test_login_page_loads_correct_form(self, client): 
        response = client.get('/login')
        assert isinstance(response.context['form'], AuthenticationForm)

