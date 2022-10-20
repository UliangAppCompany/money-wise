from django.shortcuts import render

# Create your views here.
def account_management(request, user_id): 
    return render(request, 'frontend/account_management.html')