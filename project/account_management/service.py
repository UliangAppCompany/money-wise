from datetime import datetime
from typing import Optional
from pytz import timezone

from django.conf import settings

TZ = timezone(settings.TIME_ZONE) 

def record_balance(ledger, account_number, *,  debit_amount=0, credit_amount=0, description='',
                    transaction_timestamp:Optional[str]=None, fmt = '%Y-%m-%d %H:%M:%S'): 
    account = ledger.get_account(number=account_number) 

    transaction_timestamp = datetime.strptime(transaction_timestamp, fmt).replace(tzinfo=TZ) if transaction_timestamp else datetime.now(tz=TZ) 

    account.create_balance(debit_amount=debit_amount, credit_amount=credit_amount,  
        date=transaction_timestamp, description=description)

    return account