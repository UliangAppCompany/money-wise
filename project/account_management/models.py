from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
"""
Journals are a collection of Entries. 
Entries are a collection of Transactions, date of transaction and description of transaction.  
Transactions contain an account reference and a debit/crediting amount. 

Ledgers are a collection of Accounts. 
Accounts are a collection of Balances, identified by an account number, description and can be classisfied 
    as one of Assets, Liabilities, Equity, Revenue and Expenses, and whether it is a debit or credit account.    
    
    ControlAccounts are Accounts which summarize the balance of many sub-accounts under their control. When 
        Entries are posted from the Journal to the Ledger, both ControlAccount and Account balances 
        are updated. The most recent balance of the ControlAccount must equals the total most recent balances 
        of all Accounts under its control.

        Examples of ControlAccounts are Cash, Accounts Payable, Accounts Receivable, Salaries, Inventory, 
        Fixed Assets. 
        
Balances contain a journal reference, a debit/credit amount and credit/debit balances, date of transaction and 
    description of transaction.   

    [Brought|Carry]ForwardBalances are a special kind of balances without debit/credit amount but consist only of a (preset) 
    date of transaction, a default description and credit/debit balance only. 
        
        BroughtForwardBalances are created at the start of one accounting cycle from the previous cycle's CarryForwardBalance.
        CarryForwardBalances are used to prepare trial balances and populate financial statments. 

When a new Entry is made in a Journal, it triggers a corresponding balance entry into the affected accounts. 
    Several validation checks must pass:
        The total credit and debit amounts of transactions must be equal.  
        The CarryForwardBalance = BroughtForwardBalance + net transaction amounts 
        Balance of ControlAccounts = total balance of Accounts under ControlAccount's control

Entity relationships
    Journal <- (1..*)  Entry <- (1..*) Transaction 
    Ledger <- (1..*) Account <- (1..*) Balance
    ControlAccount <- (1..*) Account
    CarryForwardBalance <- (1..1) BroughtForwardBalance <- (1..*) Balance 

"""

class Account(models.Model):
    number = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    should_debit_balance = models.BooleanField(default=True)
    credit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    debit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    category = models.ForeignKey(
        "AccountCategory", on_delete=models.CASCADE, related_name="accounts"
    )

    def __repr__(self) -> str:
        return f"<{self.number}-{self.description}>"

    @property
    def balance(self):
        return (
            self.debit_balance - self.credit_balance
            if self.should_debit_balance
            else self.credit_balance - self.debit_balance
        )


class AccountCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    supercategory = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="subcategories", null=True
    )

    def __repr__(self):
        return f"<{self.name}>"

    def get_all_category_accounts(self):
        stack = [self]
        resultset = []
        while stack:
            cat = stack.pop()
            qs = Account.objects.filter(category=cat)
            if qs.count():
                resultset.extend([account for account in qs.all()])
            else:
                stack.extend([subcat for subcat in cat.subcategories.all()])
        return resultset

    def get_category_subtotals(self):
        return sum(account.balance for account in self.get_all_category_accounts())
