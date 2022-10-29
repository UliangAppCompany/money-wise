from django import forms
from account_management.models import Account

class AccountManagementAccount(forms.ModelForm):
    class Meta: 
        model = Account
        fields = ['number', 'description', 'debit_account'] 
                
class AuthenticationForm(forms.Form): 
    username = forms.EmailField(required=True, max_length=100) 
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)