from django.urls import path 

from frontend import views 


urlpatterns = [
    path('ledger/<int:ledger_id>/account', views.add_account, name='add-account'), 
    path('ledger/<int:ledger_id>', views.ledger_management, name='ledger-page')
]