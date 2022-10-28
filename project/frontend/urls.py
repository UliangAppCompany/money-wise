from django.urls import path 

from frontend import views 


urlpatterns = [
    path('user/<int:user_id>/account', views.account_management, name='account-management'), 
    path('login', views.login_page, name="login-page")
]