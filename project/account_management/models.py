import contextlib
from typing import Literal
from account_management.exceptions import DoubleEntryError, IncorrectEntryFormatError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import Signal 



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
    Entry <- (1..*) Balance
    Account <- (1..*) Transaction 
"""

class Balance(models.Model): 
    """
    Balances contain a journal reference, a debit/credit amount and credit/debit balances, date of transaction and 
    description of transaction.   

    [Brought|Carry]ForwardBalances are a special kind of balances without debit/credit amount but consist only of a (preset) 
    date of transaction, a default description and credit/debit balance only. 
        
        BroughtForwardBalances are created at the start of one accounting cycle from the previous cycle's CarryForwardBalance.
        CarryForwardBalances are used to prepare trial balances and populate financial statments. 
    """
    class Meta: 
        ordering = ['-date']
    journal_entry = models.ForeignKey("Entry", on_delete=models.CASCADE, null=True) 
    
    date = models.DateTimeField()
    debit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  
    credit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  
    debit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)  
    credit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.TextField()   

    account = models.ForeignKey("Account", on_delete=models.CASCADE, 
        related_name="balances", null=True)


class Account(models.Model):
    """
    Accounts are a collection of Balances, identified by an account number, description and can be classisfied 
    as one of Assets, Liabilities, Equity, Revenue and Expenses, and whether it is a debit or credit account.    
    
    ControlAccounts are Accounts which summarize the balance of many sub-accounts under their control. When 
        Entries are posted from the Journal to the Ledger, both ControlAccount and Account balances 
        are updated. The most recent balance of the ControlAccount must equals the total most recent balances 
        of all Accounts under its control.

        Examples of ControlAccounts are Cash, Accounts Payable, Accounts Receivable, Salaries, Inventory, 
        Fixed Assets. 

    """
    class Meta: 
        ordering = ['number'] 

    ledger = models.ForeignKey("Ledger", on_delete=models.CASCADE, related_name="accounts", null=True)
    number = models.IntegerField()
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True) 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True) 
    debit_account = models.BooleanField(default=True)
    
    class AccountType(models.TextChoices): 
        ASSET = 'AS', _('Asset') 
        LIABILITY = 'LB', _('Liability') 
        EQUIIY = 'EQ', _('Equity') 
        REVENUE = 'RV', _('Revenue') 
        EXPENSE = 'EX', _('Expense')
    
    category = models.CharField(max_length=2, choices=AccountType.choices, default=AccountType.ASSET)

    control = models.ForeignKey('self', on_delete=models.CASCADE, related_name="subaccounts", null=True
        ,default=None)
    is_control = models.BooleanField(default=False)

    def __repr__(self) -> str:
        return f"Account({self.number}-{self.description})"

    def add_subaccounts(self, *accounts): 
        self.subaccounts.add(*accounts) 
        self.save() 

    def categorize(self, number): 
        ledger = self.ledger
        control_account = ledger.get_account(number=number)  
        control_account.add_subaccounts(self) 
        
    def create_balance(self, *, description, date, debit_amount=0, credit_amount=0): 
        latest = None
        with contextlib.suppress(Balance.DoesNotExist): 
            latest = self.balances.latest('date')
        latest_debit_balance, latest_credit_balance = 0,0
        if latest: 
            latest_debit_balance = latest.debit_balance 
            latest_credit_balance = latest.credit_balance 
        
        if self.debit_account: 
            latest_debit_balance += debit_amount - credit_amount 
        else: 
            latest_credit_balance +=  credit_amount - debit_amount
        
        current = Balance.objects.create(date=date, 
            debit_amount=debit_amount, credit_amount=credit_amount, 
            debit_balance=latest_debit_balance, credit_balance=latest_credit_balance,
            description=description)
        
        self.balances.add(current)
        self.save()
        return current
 
        
    # @property
    # def balance(self):
    #     return (
    #         self.debit_balance - self.credit_balance
    #         if self.should_debit_balance
    #         else self.credit_balance - self.debit_balance
    #     )


class Ledger(models.Model): 
    """
    Ledgers are a collection of Accounts. 
    """
    number = models.IntegerField()
    name = models.CharField(max_length=100) 
    description = models.TextField() 
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey("registration.User", on_delete=models.CASCADE, related_name='ledgers', 
        null=True )

    @property 
    def chartofaccounts(self): 
        return self.accounts

    def get_account(self, number): 
        return self.accounts.filter(number=number).get() 

    def create_account(self, number, description, category,debit_account=True,  
                        created_on=None): 
        params = {'number': number, 'description': description, 'debit_account': debit_account, 
            'category': category}  
        params |= {'created_on': created_on} if created_on else {} 

        account = Account.objects.create(**params)
        
        self.accounts.add(account) 
        self.save()

        return account 


class Transaction(models.Model): 
    """
    Transactions contain an account reference and a debit/crediting amount. 
    """ 
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    entry = models.ForeignKey("Entry", on_delete=models.CASCADE, 
        related_name="transactions", null=True)
    debit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.TextField()



class Entry(models.Model): 
    """
    Entries are a collection of Transactions, date of transaction and description of transaction.  
    """
    date = models.DateTimeField() 
    note = models.TextField(blank=True, default=None)

    journal = models.ForeignKey("Journal", on_delete=models.CASCADE, 
        related_name="entries") 


class Journal(models.Model): 
    """
    Journal is a collection of entries. 
    """
    number = models.IntegerField()
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True) 
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey('registration.User', on_delete=models.CASCADE, related_name='journals', 
        null=True)

    double_entry_created = Signal() 

    def __repr__(self): 
        return f"Journal({self.number} - {self.name})" 

    def check_valid_double_entry(self, transactions): 
        return sum(t.debit_amount - t.credit_amount for t in transactions) == 0

    def create_double_entry(self, date, note, transactions):
        if not self.check_valid_double_entry(transactions): 
            raise DoubleEntryError()        

        entry = Entry.objects.create(date=date, note=note, journal=self) 
        entry.transactions.add(*transactions)
        entry.save()

        self.double_entry_created.send(sender=Entry, instance=entry)
        return entry

