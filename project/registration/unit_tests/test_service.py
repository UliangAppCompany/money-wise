import pytest 

from django.core import mail 

from registration.exceptions import DuplicateUserNameError
from registration.service import create_user 



@pytest.mark.django_db
@pytest.mark.usefixtures("register_new_user")
def test_create_new_user_service_creates_new_user_if_not_present(cursor): 
    result = cursor.execute("select username from auth_user ").fetchone() 
    assert result == ('john@example.com', )  

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user")
def test_that_new_user_cannot_be_created_if_already_present(): 

    with pytest.raises(DuplicateUserNameError) as exc: 
        create_user('john@example.com', 'p@s$w0rd')
    
        assert str(exc) == "User john@example.com already registered."

@pytest.mark.django_db 
@pytest.mark.usefixtures("register_new_user")
def test_that_validation_email_is_sent_when_new_user_is_successfully_saved_in_db(): 
    assert len(mail.outbox) == 1    
    message = mail.outbox[0] 

    assert message.subject == "New user validation link" 
    assert message.from_email == "admin@money-wise.com.my"
    assert message.to == ["john@example.com"]
