from django import forms
from account_management.models import Account

class AccountManagementAddAccountForm(forms.ModelForm):
    class Meta: 
        model = Account
        fields = ['number', 'name', 'description', 'notes', 'debit_account'] 
                
class AuthenticationForm(forms.Form): 
    username = forms.EmailField(required=True, max_length=100) 
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)

class ChangePasswordForm(forms.Form): 
    password = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    retype_password = forms.CharField(widget=forms.PasswordInput(), max_length=100)
