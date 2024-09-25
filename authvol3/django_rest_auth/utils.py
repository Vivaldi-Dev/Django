import random
from django.core.mail import EmailMessage
from .models import User, OnetimePassword
from django.conf import settings

def generateOtp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1, 9))
    return otp    

def send_code_to_user(email):
    Subject = "One time passcode for Email verification"
    otp_code = generateOtp()
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise ValueError("User with the provided email does not exist.")
    
    current_site = "myAuth.com"
    email_body = (f"Hi {user.first_name},\n\n"
                  f"Thanks for signing up on {current_site}. "
                  f"Please verify your email using the following one-time passcode: {otp_code}\n\n"
                  "If you didn't request this, please ignore this email.")

    
    OnetimePassword.objects.create(user=user, code=otp_code)
    
   
    from_email = "no-reply@myAuth.com" 
    
    d_email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    d_email.send(fail_silently=True)

def send_normal_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body = data['email_body'],
        from_email= settings.EMAIL_HOST_USER,
        to = [data['to_email']]
    )
    email.send()