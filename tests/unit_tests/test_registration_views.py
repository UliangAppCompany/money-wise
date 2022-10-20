
def test_validation_url(client): 
    response = client.get('/registration/validate?token=abc')

    assert response.status_code == 302
