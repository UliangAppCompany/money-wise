from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model 
from django.conf import settings
from django.core.mail import send_mail 


@receiver(post_save, sender=get_user_model()) 
def send_message(sender, **kwargs): 
    user = kwargs.pop("instance") 
    if kwargs['created']: 
        user_email = user.email 
        subject = "New user validation link" 
        message = ''
        send_mail(subject, message, from_email=None, recipient_list=[user_email])

        

