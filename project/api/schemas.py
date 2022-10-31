from ninja import ModelSchema, Schema

from django.contrib.auth import get_user_model


class UserSchema(Schema): 
    username: str 
    password: str


class UserResponseSchema(ModelSchema): 
    class Config: 
        model = get_user_model() 
        model_exclude = ['password', 'validation_token']