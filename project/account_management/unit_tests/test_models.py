# from django.test import TestCase

# Create your tests here.
import pytest
from account_management.models import *


@pytest.mark.django_db
def test_initialize_objects_in_database(cursor):
    current_asset = AccountCategory.objects.create(
        name="Current Asset",
    )
    cash_account = Account(number=1, category=current_asset)

    cash_account.save()

    cursor.execute("select * from account_management_account")
    assert len(cursor.fetchall()) == 1


@pytest.mark.django_db
@pytest.mark.usefixtures("setup_fake_accounts")
@pytest.mark.parametrize("pk,result", [(1, 10), (2, 2), (7, 35 - 12)])
def test_balance_property_returns_correct_balance(pk, result):
    account = Account.objects.get(id=pk)
    assert account.balance == result

@pytest.mark.django_db 
@pytest.mark.usefixtures("setup_fake_accounts") 
@pytest.mark.parametrize('pk,resultset', [
    (1, ['Current Assets', 'Fixed Assets']), 
    (2, ['Cash', 'Accounts Receivable']), 
    (5, ['Equipment', 'Property']), 
    (8, ['Current Liabilities']), 
    (9, ['Accounts Payable']), 
    (11, ['Retained earnings']), 
    (13, ['Salaries', 'Rents']), 
    (16, ['Interest', 'Depreciation']) ])
def test_subcategories_retrievable_from_parent_category(pk, resultset): 
    account_category = AccountCategory.objects.get(id=pk)
    assert resultset == [subcat.name for subcat in account_category.subcategories.all()] 

@pytest.mark.django_db 
@pytest.mark.usefixtures('setup_fake_accounts') 
@pytest.mark.parametrize('pk,result', [
    (3, [1001, 1002]), 
    (4, [1011, 1012]), 
    (6, [1051]) , 
    (7, [1061]) ,
    (5, [1051, 1061]) , 
    (2, [1001, 1002, 1011, 1012]) , 
    (1, [1001, 1002, 1011, 1012, 1051,1061])
])  
def test_AccountCategory_get_all_accounts_method_returns_all_accounts_in_group(pk, result): 
    category = AccountCategory.objects.get(id=pk) 
    
    assert set(result) == {account.number for account in category.get_all_category_accounts()}

@pytest.mark.django_db 
@pytest.mark.usefixtures('setup_fake_accounts') 
@pytest.mark.parametrize('pk,result', [
    (3, 30-20+7-5), 
    (4, 100.5+12.), 
    (2, 100.5+12+7-5+30-20), 
    (6, 100_000) , 
    (7, 350_000) , 
    (5, 450_000), 
    (1, 30-20+7-5+100.5+450_000+12)
])
def test_get_category_balance_subtotal(pk, result): 
    category = AccountCategory.objects.get(id=pk) 
    assert result == category.get_category_subtotals()
    