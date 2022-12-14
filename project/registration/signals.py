import urllib.parse

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model 
from django.core.mail import send_mail 
from django.conf import settings


@receiver(post_save, sender=get_user_model()) 
def send_message(sender, **kwargs): 
    user = kwargs.pop("instance") 
    if kwargs['created'] and user.require_validation and not user.is_validated: 
        user_email_field = user.get_email_field_name() 
        user_email = getattr(user, user_email_field) 

        subject = "New user validation link" 
        validation_url = urllib.parse.urljoin(settings.HOSTNAME,
            f'/registration/validate?username={user.username}&token={user.validation_token}')
        message = f'Please click here to validate your email:{validation_url}' 
        
        send_mail(subject, message, from_email=None, recipient_list=[user_email])

        

