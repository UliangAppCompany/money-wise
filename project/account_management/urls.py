from django.urls import path
import account_management.views.account_category
import account_management.views.account


urlpatterns = [
    path("account-management/", account_management.views.account_category.api.urls),
    path("account-management/", account_management.views.account.api.urls),
]
