from ninja import NinjaAPI 

from django.shortcuts import render

# Create your views here.

api = NinjaAPI(version='1')

@api.post("account", url_name='add-new-account')
def add_account(request): 
    ...


