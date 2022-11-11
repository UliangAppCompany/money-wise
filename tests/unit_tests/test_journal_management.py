import pytest 

from django.test import override_settings

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

@pytest.mark.usefixtures('init_john', 'login_john')
class TestJournalApiEndpoint: 
    def post_response(self, client, url, payload): 
        response = client.post(url, data=payload, 
            content_type='application/json' )
        return response

    # @override_settings(DEBUG=True)
    @pytest.mark.parametrize('url,payload', [
        ('/api/account-management/journal', {
            'number': 1, 
            'name': 'Company A Journal', 
            'description': 'description' 
        })
    ])
    def test_that_post_endpoint_responds(self,url, payload, client):
        response = self.post_response(client, url, payload)
        assert response.status_code == 200

    @pytest.mark.parametrize('url,payload', [
        ('/api/account-management/journal', {
            'number': 1, 
            'name': 'Company A Journal', 
            'description': 'description' 
        })
    ])

    def test_that_unauthenticated_user_cannot_create_journals(self, url, payload, client): 
        client.logout()
        response = self.post_response(client, url, payload)
        assert response.status_code == 401

    @pytest.mark.parametrize('url,payload', [
        ('/api/account-management/journal', {
            'number': 1, 
            'name': 'Company A Journal', 
            'description': 'description' 
        })
    ])
    def test_that_post_endpoint_responds(self,url, payload, client, cursor):
        self.post_response(client, url, payload) 

        cursor.execute("select name from account_management_journal where "
            " number = 1 and account_management_journal.user_id = ( "
            " select id from registration_user where username = 'john@example.com' )")
        result = cursor.fetchone()

        assert result == ("Company A Journal", )

