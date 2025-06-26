from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import random
from app_modules.adminapp.models import User
from django.shortcuts import redirect
from django.contrib import messages


@shared_task
def send_password_reset_email(password,user_email):
    
    subject = "Password Reset Request"
    message = f"Your password is {password} after we you login, please change your password."
    from_email = settings.EMAIL_HOST_USER
    try:
        send_mail(subject,message,from_email,[user_email])
        print("mail send.........")
    except Exception as e:
        return f'Error sending email: {str(e)}'
        

# Change password or redirect to reset password with  user logged in
