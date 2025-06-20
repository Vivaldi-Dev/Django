from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        if not email:
            raise ValueError('users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        
        user.set_password(password)
        user.save()


class UserAccount(AbstractBaseUser,PermissionsMixin):
    email= models.EmailField(("email"), max_length=254 , unique=True)
    name = models.CharField(("nome do usuario") , max_length=266)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def get_full_name(self):
        return
    
    def get_short_name(self):
        return self.name
    
    def __str__(self):
        return self.email
    
    

