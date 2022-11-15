from django.dispatch import receiver 

from account_management.models import Entry, Journal


@receiver(Journal.double_entry_created, sender=Entry) 
def record_balances_in_account(sender, **kwargs): 
    entry = kwargs.get('instance')
    for transaction in entry.transactions.all(): 
        account = transaction.account
        account.create_balance(description=entry.note, 
                date=entry.date, 
                debit_amount=transaction.debit_amount, 
                credit_amount=transaction.credit_amount)

