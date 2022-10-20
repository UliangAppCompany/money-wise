from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model 
from django.conf import settings
from django.core.mail import send_mail 


@receiver(post_save, sender=get_user_model()) 
def send_message(sender, **kwargs): 
    user = kwargs.pop("instance") 
    if kwargs['created']: 
        user_email_field = user.get_email_field_name() 
        user_email = getattr(user, user_email_field) 
        subject = "New user validation link" 
        message = f'Please click here to validate your email: https://example.com/registration/user/{user.id}/validate?token={user.validation_token}'
        send_mail(subject, message, from_email=None, recipient_list=[user_email])

        

