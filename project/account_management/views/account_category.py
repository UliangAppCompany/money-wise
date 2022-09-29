from typing import Optional
import ninja
# from ninja import NinjaAPI 
from account_management.models  import AccountCategory
from account_management.api import SupercategoryUnavailableError, api

# Create your views here.


class AccountCategoryResponseSchema(ninja.ModelSchema):
    supercategory: 'AccountCategoryResponseSchema' = None 
    class Config: 
        model=AccountCategory
        model_fields = ['id','name', 'description']


AccountCategoryResponseSchema.update_forward_refs()

class AccountCategoryRequestSchema(ninja.ModelSchema): 
    supercategory: Optional[int] 
    class Config: 
        model=AccountCategory
        model_fields = ['name', 'description']


@api.post('/account-category', response={201: AccountCategoryResponseSchema})
def post_new_category(request, data:AccountCategoryRequestSchema): 
    cat = AccountCategory(name=data.name, description=data.description)
    if data.supercategory is not None:
        try:  
            parent_cat = AccountCategory.objects.get(id=data.supercategory)
        except AccountCategory.DoesNotExist: 
            raise SupercategoryUnavailableError()
        cat.supercategory = parent_cat
    cat.save()
    return 201, cat 

