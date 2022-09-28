import pytest
from django.db import connection


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
                (4, 'Accounts Receivable', 2), 
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
                (2, 1002, 'Petty cash', '2022-09-27 23:58:00', '2022-09-27 23:58:00', true, 5., 7., 3),  
                (3, 1011, 'Company A', '2022-09-28 14:15:00', '2022-09-28 14:15:00', true, 0., 12., 4), 
                (4, 1012, 'Company B', '2022-09-28 14:15:00', '2022-09-28 14:15:00', true, 0., 100.50, 4), 
                (5, 1051, 'Company Car', '2022-09-28 14:15:00', '2022-09-28 14:15:00', true, 0., %s, 6), 
                (6, 1061, 'Office Premises', '2022-09-28 14:15:00', '2022-09-28 14:15:00', true, 0., %s, 7), 
                (7, 2001, 'Company Credit Card', '2022-09-28 07:41:00', '2022-09-28 07:41:00', false, 35., 12., 9);
                """,
        [100_000.00, 350_000.00],
    )
