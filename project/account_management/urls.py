from django.urls import path
import account_management.views.account_category 

urlpatterns = [
    path('account-management/', account_management.views.account_category.api.urls)
]