import pytest 
from django.db import connection 
from registration.service import create_user


@pytest.fixture
def cursor():
    cursor_ = connection.cursor()
    yield cursor_ 
    cursor_.close()

@pytest.fixture 
def register_new_user(): 
    create_user('john@example.com', 'password') 

    
