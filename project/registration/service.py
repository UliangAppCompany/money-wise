from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from registration.exceptions import DuplicateUserNameError  


def create_user(username, token=None, **save_kwargs): 
    User = get_user_model() 
    try: 
        user = User(username=username)
        if token: 
            user.validation_token = token
        user.save(**save_kwargs)
    except IntegrityError: 
        raise DuplicateUserNameError(f"User {username} already registered.")
    return user


def create_validated_user(username, password=None): 
    User = get_user_model() 
    try: 
        user = User(username=username, is_validated=True)
        if password: 
            user.set_password(password)  
        user.save()
        return user
    except: 
        raise DuplicateUserNameError(f"User {username} already registered.")