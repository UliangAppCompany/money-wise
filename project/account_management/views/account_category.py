from typing import Optional
import ninja

# from ninja import NinjaAPI
from account_management.models import AccountCategory
from account_management.views import SupercategoryUnavailableError, api
from account_management.views import DuplicateValueError

# Create your views here.


class AccountCategoryResponseSchema(ninja.ModelSchema):
    supercategory: "AccountCategoryResponseSchema" = None

    class Config:
        model = AccountCategory
        model_fields = ["id", "name", "description"]


AccountCategoryResponseSchema.update_forward_refs()


class AccountCategoryRequestSchema(ninja.ModelSchema):
    supercategory: Optional[int]

    class Config:
        model = AccountCategory
        model_fields = ["name", "description"]


@api.get("/account-category", response={200: list[AccountCategoryResponseSchema]})
def get_account_categories(request):
    cats = AccountCategory.objects.all()
    return 200, cats


@api.post("/account-category", response={201: AccountCategoryResponseSchema})
def post_new_category(request, data: AccountCategoryRequestSchema):
    if AccountCategory.objects.filter(name=data.name).exists():
        raise DuplicateValueError(
            f"Account Category named '{data.name}' already exists."
        )

    cat = AccountCategory(name=data.name, description=data.description)
    if data.supercategory is not None:
        try:
            parent_cat = AccountCategory.objects.get(id=data.supercategory)
        except AccountCategory.DoesNotExist:
            raise SupercategoryUnavailableError()
        cat.supercategory = parent_cat
    cat.save()
    return 201, cat
