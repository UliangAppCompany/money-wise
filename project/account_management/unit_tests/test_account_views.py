import pytest


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_fake_accounts")
@pytest.mark.parametrize("pk,resource", [(1, {"id": 1, "number": 1001})])
def test_get_account(pk, resource, client):
    response = client.get(f"/api/account-management/account/{pk}")

    assert response.status_code == 200
    assert response.json() == resource
