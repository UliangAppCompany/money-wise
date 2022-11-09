from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model() 

def create_user(username, token=None, password=None, is_validated=False, require_validation=True): 
    if User.objects.filter(username=username).exists(): 
        raise IntegrityError(f'User {username} already registered.')
    user = User(username=username, require_validation=require_validation, is_validated=is_validated)
    user.generate_validation_token(token)
    if password: 
        user.set_password(password)
    user.save()
    return user

def validate_user(user:User) -> User : 
    if not user.is_validated:
        user.is_validated= True
        user.save()
    return user 

def get_user(username:str) -> User: 
    return User.objects.get(username=username) 


