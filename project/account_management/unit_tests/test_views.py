import pytest


@pytest.fixture
def setup_initial_category(cursor):
    cursor.execute(
        """
            insert into account_management_accountcategory 
            (id, name, supercategory_id) 
            values 
            (1, 'Assets', null); 
            """
    )


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_initial_category")
def test_post_new_category_returns_created_response(client):

    response = client.post(
        "/api/account-management/account-category",
        {
            "name": "Cash",
            "description": "All liquid assets stored in bank or petty cash",
            "supercategory": 1,
        },
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 2,
        "name": "Cash",
        "description": "All liquid assets stored in bank or petty cash",
        "supercategory": {
            "id": 1,
            "name": "Assets",
            "description": None,
            "supercategory": None,
        },
    }


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_initial_category")
def test_after_post_database_is_updated(cursor, client):
    client.post(
        "/api/account-management/account-category",
        {
            "name": "Cash",
            "description": "All liquid assets stored in bank or petty cash",
            "supercategory": 1,
        },
        content_type="application/json",
    )

    cursor.execute("select * from account_management_accountcategory")
    assert len(cursor.fetchall()) == 2


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_initial_category")
def test_relationship_between_category_is_reflected_in_the_model(client, cursor):

    client.post(
        "/api/account-management/account-category",
        {
            "name": "Cash",
            "description": "All liquid assets stored in bank or petty cash",
            "supercategory": 1,
        },
        content_type="application/json",
    )

    client.post(
        "/api/account-management/account-category",
        {
            "name": "Accounts Receivable",
            "description": "Vendors that owe us money for goods sold.",
            "supercategory": 1,
        },
        content_type="application/json",
    )

    cursor.execute(
        """
        select name from account_management_accountcategory
        where supercategory_id = 1 
        """
    )
    assert cursor.fetchall() == [("Cash",), ("Accounts Receivable",)]


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_initial_category")
def test_post_base_account_category(client):
    response = client.post(
        "/api/account-management/account-category",
        {
            "name": "Liabilities",
            "description": "Liability accounts",
            "supercategory": None,
        },
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 2,
        "name": "Liabilities",
        "description": "Liability accounts",
        "supercategory": None,
    }


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_initial_category")
def test_400_error_is_raised_when_parent_category_is_not_detected(client):
    response = client.post(
        "/api/account-management/account-category",
        {
            "name": "Liabilities",
            "description": "Liability accounts",
            "supercategory": 0,
        },
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json()["message"] == "Parent category not found."


def test_documentation_page_loads_from_the_correct_url(client):
    response = client.get("/api/account-management/docs")

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_fake_accounts")
def test_list_of_account_categories(client):
    response = client.get("/api/account-management/account-category")

    assert response.status_code == 200
    assert len(response.json()) == 18


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_initial_category")
def test_cannot_add_duplicate_account_category_name(client):
    response = client.post(
        "/api/account-management/account-category",
        {"name": "Assets", "description": None, "supercategory": None},
        content_type="application/json",
    )

    assert response.status_code == 403
    assert (
        response.json()["message"] == "Account Category named 'Assets' already exists."
    )


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_fake_accounts")
@pytest.mark.parametrize(
    "pk,resource",
    [
        (1, {"id": 1, "name": "Assets", "description": None, "supercategory": None}),
        (
            2,
            {
                "id": 2,
                "name": "Current Assets",
                "description": None,
                "supercategory": {
                    "id": 1,
                    "name": "Assets",
                    "description": None,
                    "supercategory": None,
                },
            },
        ),
        (
            10,
            {
                "id": 10,
                "name": "Accounts Payable",
                "description": None,
                "supercategory": {
                    "id": 9,
                    "name": "Current Liabilities",
                    "description": None,
                    "supercategory": {
                        "id": 8,
                        "name": "Liabilities",
                        "description": None,
                        "supercategory": None,
                    },
                },
            },
        ),
    ],
)
def test_get_account_category(pk, resource, client):
    response = client.get(f"/api/account-management/account-category/{pk}")

    assert response.status_code == 200
    assert response.json() == resource
