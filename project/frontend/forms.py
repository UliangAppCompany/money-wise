from django import forms
from account_management.models import Account

class AccountManagementAddAccountForm(forms.ModelForm):
    class Meta: 
        model = Account
        fields = ['number', 'name', 'description', 'notes', 'debit_account'] 
                
        