from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from registration.exceptions import DuplicateUserNameError  

def create_user(username, password): 
    User = get_user_model() 
    try: 
        User.objects.create_user(username, username, password)
    except IntegrityError: 
        raise DuplicateUserNameError(f"User {username} already registered.")
