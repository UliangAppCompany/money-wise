from django.urls import path 

from frontend import views 


urlpatterns = [
    path('ledger/<int:ledger_id>/account', views.add_account, name='add-account'), 
    path('ledger/<int:ledger_id>', views.ledger_page, name='ledger-page'), 
    path('login', views.login_page, name="login-page"),
    path('user/<int:user_id>/set-password', views.set_password_page, name="set-password-page"), 
    path('validate', views.validate_registration, name="validated-registration" )

]