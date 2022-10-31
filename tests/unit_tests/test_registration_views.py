import pytest 

@pytest.mark.django_db
@pytest.mark.usefixtures("register_new_user")
def test_validation_url(client): 
    response = client.get('/registration/validate?username=john@example.com&token=abc')

    assert response.status_code == 302
