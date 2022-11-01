from dateutil import parser

import pytest


pytestmark = [
    pytest.mark.django_db, 
    pytest.mark.usefixtures("register_new_user", "validate_new_user", 
        "login_user")]


@pytest.fixture
def post_response(client): 
    response = client.post('/api/ledger', data={'number': 1, 'name': 'Company A General Ledger', 
        "description": "Description"}, content_type="application/json")  
    
    return response


def test_that_can_add_ledger_to_user(post_response): 
    assert post_response.status_code == 200 

def test_that_ledger_is_added_to_database(post_response, cursor): 
    cursor.execute("select * from account_management_ledger where user_id = ( " 
        " select id from registration_user where username='john@example.com') ")

    result = cursor.fetchall()
    assert len(result) != 0


def test_that_response_returns_json(post_response): 
    parsed_object = post_response.json()

    assert ['id', 'number', 'name', 'description', 'created_on', 'updated_on'] == list(parsed_object.keys())

def test_that_unauthenticated_user_cannot_post_to_endpoint(client): 
    client.logout()
    response = client.post('/api/ledger', data={'number': 1, 'name': 'Company A General Ledger', 
        "description": "Description"}, content_type="application/json")  

    assert response.status_code == 401 