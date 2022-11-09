import secrets

from ninja import  Router
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from ..schemas import UserResponseSchema, UserSetPasswordSchema
from ..exceptions import ApiAuthError


router = Router()

@router.patch('/user/{user_id}', response=UserResponseSchema)
def patch_user(request, user_id:int, data:UserSetPasswordSchema):
    if not secrets.compare_digest(data.password, data.retype_password): 
        raise ApiAuthError("Password does not match")
    user = get_object_or_404(get_user_model(), id=user_id) 
    if not user.is_validated: 
        raise ApiAuthError("User is not validated") 
    user.set_password(data.password) 
    user.save() 
    return user
