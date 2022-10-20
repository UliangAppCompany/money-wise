from urllib import response


def test_add_account_page_loads(client): 
    response = client.get('/user/1/account')
    assert response.status_code == 200 