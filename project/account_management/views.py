import ninja
from ninja import NinjaAPI 
from account_management.models  import AccountCategory

# Create your views here.


api = NinjaAPI() 

class AccountCategoryResponseSchema(ninja.ModelSchema):
    supercategory: 'AccountCategoryResponseSchema' = None 
    class Config: 
        model=AccountCategory
        model_fields = ['id','name', 'description']


AccountCategoryResponseSchema.update_forward_refs()

class AccountCategoryRequestSchema(ninja.ModelSchema): 
    supercategory: int 
    class Config: 
        model=AccountCategory
        model_fields = ['name', 'description']


@api.post('/account-management/account-category', response={201: AccountCategoryResponseSchema})
def post_new_category(request, data:AccountCategoryRequestSchema): 
    parent_cat = AccountCategory.objects.get(id=data.supercategory)
    cat = AccountCategory(name=data.name, description=data.description)
    cat.supercategory = parent_cat
    cat.save()
    return 201, cat 
