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
    ledger = models.ForeignKey("Ledger", on_delete=models.CASCADE, related_name="accounts", null=True)
    number = models.IntegerField()
    description = models.TextField(blank=True, null=True)
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

    def __repr__(self) -> str:
        return f"Account({self.number}-{self.description})"

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

    @property 
    def chartofaccounts(self): 
        return self.accounts

    def get_account(self, number): 
        return self.accounts.filter(number=number).get() 

    def create_account(self, number, description, debit_account, category, 
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
    date = models.DateTimeField(auto_now=True) 
    notes = models.TextField(blank=True, default=None)

    journal = models.ForeignKey("Journal", on_delete=models.CASCADE, 
        related_name="entries") 


TransDetails = dict[Literal['debit_amount'] | Literal['credit_amount'], float]


class Journal(models.Model): 
    """
    Journal is a collection of entries. 
    """
    number = models.IntegerField()
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True) 
    created_on = models.DateTimeField(auto_now_add=True) 
    updated_on = models.DateTimeField(auto_now=True) 

    double_entry_created = Signal() 

    def __repr__(self): 
        return f"Journal({self.number} - {self.name})" 

    def create_double_entry(self, ledger, date, notes, transactions: dict[int, TransDetails]): 
        check = 0
        transaction_objects = [] 
        for account_number, trans_details in transactions.items(): 
            db_amount, cr_amount = trans_details['debit_amount'], trans_details['credit_amount']
            check += db_amount - cr_amount 
            account = ledger.get_account(number=account_number) 
            
            if db_amount and cr_amount:
                raise IncorrectEntryFormatError("No two debit amount and credit amount can be nonzero.")
            elif cr_amount and db_amount==0: 
                msg = f"from {account_number}-{account.description} account"
            else: 
                msg = f"to {account_number}-{account.description} account"
            
            transaction = Transaction(account=account,  
                debit_amount=db_amount,
                credit_amount=cr_amount, 
                description=msg)
            transaction_objects.append(transaction)

        if check: 
            raise DoubleEntryError()        
        
        Transaction.objects.bulk_create(transaction_objects)

        entry = Entry.objects.create(date=date, notes=notes, journal=self) 
        entry.transactions.add(*transaction_objects)
        entry.save()

        self.double_entry_created.send(sender=Entry, instance=entry)

