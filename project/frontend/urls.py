from django.urls import path 

from frontend import views 


urlpatterns = [
    path('ledger/<int:ledger_id>/account', views.account_management, name='account-management')
]