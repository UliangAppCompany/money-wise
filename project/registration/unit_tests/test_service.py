from registration.exceptions import DuplicateUserNameError
from registration.service import create_user 
import pytest 



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
