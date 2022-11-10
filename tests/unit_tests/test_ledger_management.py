import pytest 

pytestmark = [
    pytest.mark.django_db
]

class TestLedgerModel: 
    def test_init_ledger(self,cursor, ledger): 
        cursor.execute("select number, name from account_management_ledger "
        "where id = %s", [ledger.id]) 
        result=cursor.fetchall() 

        assert result == [(1, "Company A General Ledger")] 

    @pytest.mark.usefixtures("add_accounts_to_ledger")
    def test_ledger_create_account(self,cursor, ledger): 
        cursor.execute(
            "select number, description, debit_account, category " 
            "from account_management_account "
            "where ledger_id = %s", [ledger.id])
        
        result = cursor.fetchall()

        assert len(result) ==3  
        assert set(result) == {
            (100, "Cash", True, "AS"), 
            (200, "Checking", False, "LB"), 
            (300, "Revenue", False, "RV")
        }

    @pytest.mark.usefixtures("add_accounts_to_ledger")
    def test_get_account_from_ledger(self,ledger): 
        cash_account = ledger.get_account(number=100)
        
        assert cash_account.description == "Cash"


@pytest.mark.usefixtures("init_john", "login_john")
class TestLedgerApiEndpoint: 
    
    def post_response(self, client): 
        response = client.post('/api/account-management/ledger',
            data={'number': 1, 'name': 'Company A General Ledger', 
                "description": "Description"},
            content_type="application/json")  

        return response
    
    def test_that_can_add_ledger_to_user(self, client): 
        response = self.post_response(client)
        assert response.status_code == 200 

    def test_that_ledger_is_added_to_database(self, cursor, client): 
        self.post_response(client)
        cursor.execute("select * from account_management_ledger where user_id = ( " 
            " select id from registration_user where username='john@example.com') ")

        result = cursor.fetchall()
        assert len(result) != 0

    def test_that_unauthenticated_user_cannot_post_to_endpoint(self, client): 
        client.logout()
        response = self.post_response(client)
        assert response.status_code == 401 