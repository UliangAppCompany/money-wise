import pytest
from account_management.models import AccountCategory 

@pytest.fixture 
def setup_initial_category(cursor):
    cursor.execute('''
            insert into account_management_accountcategory 
            (id, name, supercategory_id) 
            values 
            (1, 'Assets', null); 
            ''')


@pytest.mark.django_db
@pytest.mark.usefixtures('setup_initial_category')
def test_post_new_category_returns_created_response(client): 

    response = client.post('/api/account-management/account-category', {
            'name': 'Cash', 
            'description': 'All liquid assets stored in bank or petty cash', 
            'supercategory': 1
        }, content_type='application/json') 

    assert response.status_code == 201 
    assert response.json() == {
            'id': 2, 
            'name': 'Cash', 
            'description': 'All liquid assets stored in bank or petty cash', 
            'supercategory': {
                'id': 1, 
                'name': 'Assets', 
                'description': None, 
                'supercategory': None
                } 
             }

@pytest.mark.django_db
@pytest.mark.usefixtures('setup_initial_category')
def test_after_post_database_is_updated(cursor, client): 
    client.post('/api/account-management/account-category', {
            'name': 'Cash', 
            'description': 'All liquid assets stored in bank or petty cash', 
            'supercategory': 1
        }, content_type='application/json') 

    cursor = cursor.execute('select * from account_management_accountcategory') 
    assert len(cursor.fetchall()) == 2 
    

@pytest.mark.django_db
@pytest.mark.usefixtures('setup_initial_category')
def test_relationship_between_category_is_reflected_in_the_model(client): 
    
    client.post('/api/account-management/account-category', {
            'name': 'Cash', 
            'description': 'All liquid assets stored in bank or petty cash', 
            'supercategory': 1
        }, content_type='application/json') 

    asset = AccountCategory.objects.get(id=1) 
    assert ['Cash'] == [cat.name for cat in asset.subcategories.all()]


@pytest.mark.django_db 
@pytest.mark.usefixtures("setup_initial_category") 
def test_post_base_account_category(client): 
    response = client.post('/api/account-management/account-category', {
        'name': 'Liabilities', 
        'description': 'Liability accounts', 
        'supercategory': None
    }, content_type='application/json')  

    assert response.status_code == 201 
    assert response.json() == { 
        'id':2, 
        'name': 'Liabilities', 
        'description': 'Liability accounts', 
        'supercategory': None
    }