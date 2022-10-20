import pytest 

@pytest.mark.django_db
@pytest.mark.usefixtures("register_new_user")
def test_validation_url(client): 
    response = client.get('/registration/user/1/validate?token=abc')

    assert response.status_code == 302
