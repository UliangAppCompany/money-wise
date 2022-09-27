# from django.test import TestCase

# Create your tests here.
import pytest
from django.db import connection
from account_management.models import *


@pytest.fixture
def cursor():
    cur = connection.cursor()
    yield cur
    cur.close()


@pytest.fixture
def setup_fake_accounts(cursor):
    cursor.execute(
        """
            insert into account_management_accountcategory 
                (id, name, supercategory_id)
            values 
                (1, 'Assets', null), 
                (2, 'Current Assets', 1), 
                (3, 'Cash', 2), 
                (4, 'Account Receivables', 2), 
                (5, 'Fixed Assets', 1), 
                (6, 'Equipment', 5), 
                (7, 'Property', 5), 
                (8, 'Liabilities', null), 
                (9, 'Current Liabilities',  8), 
                (10, 'Accounts Payable', 9), 
                (11, 'Capital', null), 
                (12, 'Retained earnings', 11), 
                (13, 'Revenue', null), 
                (14, 'Salaries', 13), 
                (15, 'Rents', 13), 
                (16, 'Expenses', null), 
                (17, 'Interest', 16), 
                (18, 'Depreciation', 16); 

            """
    )

    cursor.execute(
        """
            insert into account_management_account 
                (id, number, description, created_on, updated_on, should_debit_balance, credit_balance, debit_balance, category_id) 
            values 
                (1, 1001, 'Public Bank-Business account', '2022-09-27 23:58:00', '2022-09-27 23:58:00', true, 20., 30., 3), 
                (2, 1002, 'Petty cash', '2022-09-27 23:58:00', '2022-09-27 23:58:00', true, 5., 7., 3); 
                """
    )


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
@pytest.mark.parametrize('pk,result', [(1, 10), (2,2)])
def test_balance_property_returns_correct_balance(pk, result):
    account = Account.objects.get(id=pk) 
    assert account.balance == result
