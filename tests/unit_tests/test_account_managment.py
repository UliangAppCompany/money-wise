import pytest

from account_management.service import record_balance

from account_management.models import Ledger
from frontend.forms import AccountManagementAddAccountForm

pytestmark = [
    pytest.mark.django_db
]


@pytest.mark.usefixtures("add_accounts_to_ledger", "create_cash_accounts") 
class TestAccountModel: 
    def test_account_create_balance_entry(self, cursor, ledger): 
        record_balance(ledger, 100, debit_amount=1050, 
            description="being collections from cash register" )
        
        cash_account = record_balance(ledger, 100, credit_amount=950, description="being payment of invoice-XXX")

        cursor.execute(
            "select debit_amount, credit_amount, debit_balance, description " 
            "from account_management_balance "
            "where account_id = %s "
            "order by date desc", [cash_account.id])
        result = cursor.fetchall()
        
        assert pytest.approx(result) == [
            (0, 950, 100, "being payment of invoice-XXX"), 
            (1050, 0, 1050, "being collections from cash register")
        ]

    def test_that_accounts_can_be_associated_with_a_control_account(self, cursor, ledger): 
        control_account = ledger.get_account(number=100) 
        bank_account1 = ledger.get_account(number=101)
        bank_account2 = ledger.get_account(number=102)
        
        control_account.add_subaccounts(bank_account1, bank_account2)

        cursor.execute("select number, description from account_management_account "
                "where control_id = %s ", [control_account.id])

        result = cursor.fetchall()
        assert result == [(101, "Cash in Bank 1" ), (102, "Cash in Bank 2")]

    def test_that_can_add_a_control_account_to_an_account(self, cursor, ledger): 
        account = ledger.get_account(number=101) 
        account.categorize(number=100) 


        cursor.execute("select number, description from "
            "account_management_account "
            "where control_id = ( " 
            " select id from account_management_account " 
            " where number=100 and ledger_id = %s)", 
        [ledger.id]) 

        result = cursor.fetchall()
        assert result == [(101, "Cash in Bank 1")]


@pytest.mark.usefixtures('init_john', 'john_adds_ledger', 'login_john')
class TestAccountApiEndpoint: 
    def post_response(self, client, ledger): 
        response = client.post(f'/api/account-management/ledger/{ledger.id}/account', data={
            'number': 100, 
            'name': 'Cash', 
            "description": "Description", 
            "notes": "Cash on hand.", 
            'category': "AS", 
            'is_control': False, 
            "debit_account": True}, 
        content_type="application/json")  
        
        return response

    def test_add_account_view_returns_ok_status(self, client, ledger): 
        response = self.post_response(client, ledger)
        assert response.status_code == 200 

    def test_add_account_view_adds_resource_to_db(self, client, ledger, cursor): 
        self.post_response(client, ledger)

        cursor.execute("select * from account_management_account "
            " join account_management_ledger on account_management_account.ledger_id = account_management_ledger.id " 
            " where account_management_account.number = 100 "
            " and account_management_ledger.user_id = (select id from registration_user " 
            " where username = 'john@example.com')")
        result = cursor.fetchall()

        assert len(result) != 0 

    def test_that_cannot_make_unauthenticated_api_calls(self, client, ledger): 
        client.logout()
        response = self.post_response(client, ledger)
        assert response.status_code == 401
            
@pytest.mark.usefixtures(
    "create_current_account",
    "init_john", 
    "john_adds_ledger",
    "login_john" ) 
@pytest.mark.parametrize('url,payload', [
    ('/api/account-management/ledger/{ledger_id}/account/{account_id}', {
        'number': 100, 
        'name': 'Current Assets', 
        'description': 'description', 
        'notes': 'notes', 
        'category': 'AS', 
        'is_control': True, 
        'debit_account': True, 
        'subaccounts': [
            {
                'number': 101, 
                "name": "Cash in Bank A", 
                "description": "Deposits in Bank A", 
                "notes": "notes", 
                "category": "AS", 
                "is_control": False, 
                "debit_account": True, 
            }, 
            {
                "number": 102, 
                "name": "Petty Cash", 
                "description": "description", 
                "notes": "notes", 
                "category": "AS", 
                "is_control": False, 
                "debit_account": True
            }
        ]
    })
])
class TestAccountPutEndpoint: 
    def put_response(self, client, ledger, url, payload): 
        control_account = ledger.get_account(payload['number']) 
        payload['id'] = control_account.id
        response = client.put(url.format(ledger_id=ledger.id, account_id=control_account.id), 
            data=payload, content_type='application/json')
        return response

    def execute_sql_statement(self, cursor, control_account): 
        cursor.execute("select number from account_management_account "
            "where control_id = ( select id from account_management_account "
            "where number = %s )", [control_account.number])
        return cursor.fetchall() 

    def test_that_classifying_accounts_returns_ok_status(self, url, payload, client, ledger): 
        response = self.put_response(client, ledger, url, payload)
        
        assert response.status_code == 200

    def test_that_accounts_are_properly_classified_at_the_db_level(self, url, payload, client, ledger, cursor): 
        self.put_response(client, ledger, url, payload) 
        control_account = ledger.get_account(payload['number'])
        result = self.execute_sql_statement(cursor, control_account)

        assert result == [(suba['number'], ) for suba in payload['subaccounts'] ]

@pytest.mark.usefixtures('init_john', 'john_adds_ledger', 'login_john')
class TestAccountManagementFrontend:
    def get_response(self, client, ledger): 
        client.login(username='john@example.com', password='password')
        response = client.get(f'/ledger/{ledger.id}/account')
        return response 

    def test_add_account_page_loads(self, client, ledger): 
        response = self.get_response(client, ledger)
        assert response.status_code == 200 

    def test_template_renders_with_correct_context(self, client, ledger): 
        response = self.get_response(client, ledger)
        context = response.context
        assert isinstance(context['form'], AccountManagementAddAccountForm)  
        assert isinstance(context['ledger'], Ledger)
        assert 'account_management/add_account_page.html' in [template.name for template in response.templates]

