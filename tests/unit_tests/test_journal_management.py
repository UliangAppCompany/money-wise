import pytest 

pytestmark = [
    pytest.mark.django_db 
]

@pytest.mark.usefixtures("add_accounts_to_ledger", "collect_from_cash_register")
class TestJournalModel: 
    def test_init_journal(self, cursor, journal): 
        cursor.execute("select number, name from account_management_journal "
            "where id = %s",  [journal.id]) 
        result = cursor.fetchall()

        assert result == [(1, 'Company A Journal')]

    def test_journal_create_double_entry(self, cursor, journal): 
        cursor.execute("select notes from account_management_entry " 
                "where journal_id = %s", 
                [journal.id])
        result = cursor.fetchall() 

        assert result == [('being collections from cash register', )] 

    def test_that_transaction_database_is_updated_with_double_entry(self, cursor, journal):
        cursor.execute("select number, debit_amount, credit_amount, account_management_transaction.description "
                "from account_management_account, account_management_transaction "
                "where account_management_account.id = account_id " 
                "and entry_id in " 
                "(select id from account_management_entry "
                "where journal_id = %s) " 
                "order by number ", 
                [journal.id])
        result = cursor.fetchall()

        assert result == [
                (100, 1050, 0, "to 100-Cash account"), 
                (300, 0, 1050, "from 300-Revenue account")
                ]

    @pytest.mark.parametrize('account_num,expected', [
        (100, ("being collections from cash register", 1050, 0, 1050, 0)), 
        (300, ("being collections from cash register", 0, 1050, 0, 1050))
        ] )
    def test_that_account_balance_is_updated_after_journal_entry(self, account_num, expected, cursor, ledger): 
        cursor.execute("select account_management_balance.description, debit_amount, credit_amount, debit_balance, credit_balance " 
                "from account_management_balance "
                "join account_management_account "
                "on account_id = account_management_account.id "
                "where number = %s "
                "and ledger_id = %s ", [account_num, ledger.id] )
        result = cursor.fetchall()

        assert result == [expected]
