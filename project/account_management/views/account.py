import ninja
from ninja import NinjaAPI
from account_management.models import Account


api = NinjaAPI(urls_namespace="account")


class AccountResponseSchema(ninja.ModelSchema):
    class Config:
        model = Account
        model_fields = ["id", "number"]


@api.get("/account/{id}", response={200: AccountResponseSchema})
def get_account(request, id: int):
    acc = Account.objects.get(id=id)
    return 200, acc
