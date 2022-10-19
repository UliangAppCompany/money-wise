import pytest 
from django.db import connection 


@pytest.fixture
def cursor():
    cursor_ = connection.cursor()
    yield cursor_ 
    cursor_.close()
    
