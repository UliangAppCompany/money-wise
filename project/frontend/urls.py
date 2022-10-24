from django.urls import path 

from frontend import views 


urlpatterns = [
    path('ledger/<int:ledger_id>/account/new', views.add_new_account, name='add-new-account'), 
    path('ledger/<int:ledger_id>/account', views.list_accounts, name='list-accounts')
]