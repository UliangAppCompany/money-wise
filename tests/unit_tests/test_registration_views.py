import pytest 

from django.contrib.auth import get_user_model
from registration.service import create_validated_user

pytestmark = [
    pytest.mark.django_db
]

@pytest.mark.usefixtures("register_new_user")
def test_validation_url(client): 
    response = client.get('/registration/validate?username=john@example.com&token=abc')

    assert response.status_code == 302

@pytest.fixture 
def validated_user(): 
    user = create_validated_user('john@example.com')
    return user

def test_set_password_endpoint_returns_valid_response(client, validated_user): 
    response = client.patch(f'/api/user/{validated_user.id}', data={
        'password': 'password', 
        'retype_password': 'password'
    }, content_type='application/json')
    assert response.status_code == 200

def test_set_password_returns_error_if_passwords_do_not_match(validated_user, client): 
    response = client.patch(f'/api/user/{validated_user.id}', {
        'password': 'password', 
        'retype_password': 'p@as$word'
    }, content_type='application/json')

    assert response.status_code == 401
    assert response.json().get('message') == 'Password does not match'

def test_user_not_found_raises_404_error(client): 
    response = client.patch(f'/api/user/1', data={
        'password': 'password', 
        'retype_password': 'password' 
    }, content_type='application/json')

    assert response.status_code == 404 

@pytest.mark.usefixtures("register_new_user")
def test_unvalidated_user_cannot_set_password(client): 
    user = get_user_model().objects.get(username='john@example.com')
    response = client.patch(f'/api/user/{user.id}', {
        'password': 'password', 
        'retype_password': 'password'
    }, content_type='application/json')  

    assert response.status_code == 401
    assert response.json().get('message') == "User is not validated"
