import pytest 

from registration.service import validate_user, get_user

pytestmark = [
    pytest.mark.django_db
]

@pytest.fixture 
def validate_john(john): 
    john = validate_user(john)

@pytest.mark.usefixtures('validate_john')
class TestSetPasswordApiEndpoint: 
    def test_set_password_endpoint_returns_valid_response(self,client, john): 
        response = client.patch(f'/api/registration/user/{john.id}', data={
            'password': 'password', 
            'retype_password': 'password'
        }, content_type='application/json')
        assert response.status_code == 200

    def test_set_password_returns_error_if_passwords_do_not_match(self,john, client): 
        response = client.patch(f'/api/registration/user/{john.id}', {
            'password': 'password', 
            'retype_password': 'p@as$word'
        }, content_type='application/json')

        assert response.status_code == 401
        assert response.json().get('message') == 'Password does not match'

    def test_user_not_found_raises_404_error(self,client): 
        response = client.patch(f'/api/registration/user/1', data={
            'password': 'password', 
            'retype_password': 'password' 
        }, content_type='application/json')

        assert response.status_code == 404 

    def test_unvalidated_user_cannot_set_password(self,client): 
        john = get_user('john@example.com')
        john.is_validated=False 
        john.save()

        response = client.patch(f'/api/registration/user/{john.id}', {
            'password': 'password', 
            'retype_password': 'password'
        }, content_type='application/json')  

        assert response.status_code == 401
        assert response.json().get('message') == "User is not validated"

        