import time
from datetime import timedelta

import pytest 

from django.core import mail 
from django.test import override_settings
from django.db.utils import IntegrityError

from registration.exceptions import TokenExpiredError, UnvalidatedUserError
from registration.service import create_user, get_user, validate_user
from frontend.forms import ChangePasswordForm

pytestmark = [
    pytest.mark.django_db, 
]

class TestCreateUserFunction: 
    def test_create_new_user_service_creates_new_user_if_not_present(self, cursor): 
        create_user('john@example.com', require_validation=False)
        cursor.execute("select username from registration_user ") 
        result = cursor.fetchone()
        assert result == ('john@example.com', )  

    def test_that_new_user_cannot_be_created_if_already_present(self, ): 
        create_user('john@example.com', require_validation=False)
        with pytest.raises(IntegrityError) as exc: 
            create_user('john@example.com', require_validation=False)
        
            assert str(exc) == "User john@example.com already registered."

    def test_that_unvalidated_user_cannot_set_password(self, john): 
        with pytest.raises(UnvalidatedUserError) as exc: 
            john.set_password('password') 
            assert str(exc) == "Password cannot be set on unvalidated users."
    
    def test_that_password_can_be_set_on_users_that_do_not_require_validation(self): 
        john = create_user('john@example.com', require_validation=False, is_validated=False) 
        try: 
            john.set_password('password') 
        except UnvalidatedUserError: 
            pytest.fail('Error should not be raised.')
    
    def test_that_custom_token_can_be_set(self, cursor): 
        john = create_user('john@example.com', token='abc', require_validation=True)

        cursor.execute('select validation_token from registration_user')
        result = cursor.fetchone() 

        assert result == ('abc', )


class TestUserValidationEmail: 
    def test_that_validation_email_is_sent_when_new_user_is_successfully_saved_in_db(self, john): 
        assert len(mail.outbox) == 1    
        message = mail.outbox[0] 

        assert message.subject == "New user validation link" 
        assert message.from_email == "admin@money-wise.com.my"
        assert message.to == ["john@example.com"]
        assert f'registration/validate?username=john@example.com&token={john.validation_token}' in message.body 

    def test_that_email_is_not_sent_when_user_does_not_require_validation(self): 
        john = create_user('john@example.com', require_validation=False, is_validated=False)
        assert len(mail.outbox) == 0

    def test_that_email_is_not_sent_when_user_info_is_updated(self, john): 
        mail.outbox = [] 
        john.first_name = 'John'
        john.save()
        assert len(mail.outbox) == 0 

@pytest.fixture 
def set_validation_token(john): 
    john.is_validated= False 
    john.validation_token = 'abc' 
    john.save()

@pytest.mark.usefixtures('set_validation_token')
class TestValidationRoute: 
    def test_validation_url(self,client): 
        response = client.get('/validate?username=john@example.com&token=abc')
        assert response.status_code == 302

    def test_that_clicked_validation_link_validates_user(self,client, ): 
        response =client.get('/validate?username=john@example.com&token=abc')
        john = get_user('john@example.com')
        assert john.is_validated 

    @override_settings(
        VALIDATION_TOKEN_EXPIRY = timedelta(seconds=0.5)
    )
    def test_that_user_cannot_be_validated_if_validation_link_has_expired(self, client): 
        time.sleep(0.6) 
        with pytest.raises(TokenExpiredError):
            response = client.get('/validate?username=john@example.com&token=abc')
        john = get_user('john@example.com')
        assert not john.is_validated

    def test_that_if_token_is_incorrect_user_is_not_validated(self, client,): 
        response = client.get('/validate?username=john@example.com&token=asafsiudf')
        john = get_user('john@example.com')
        assert not john.is_validated

    def test_that_if_user_not_found_response_is_404(self, client): 
        response = client.get('/validate?username=gary@example.com&token=abc')
        assert response.status_code == 404


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

class TestSetPasswordPage: 
    def test_set_password_page_loads(self, client): 
        response = client.get('/user/1/set-password')
        assert response.status_code == 200
    
    def test_correct_form_is_loaded_in_the_set_password_page(self, client): 
        response = client.get('/user/1/set-password')
        context = response.context

        assert isinstance(context['form'], ChangePasswordForm)

    