from django.db import models
from django.core.validators import validate_integer
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin

from .managers import UserManager
from .validators import validate_phone
# Create your models here.


class User(AbstractBaseUser , PermissionsMixin):
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[validate_integer , validate_phone]
    )
    username = models.CharField(max_length=255 ,null=True , blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def __str__(self) -> str:
        return self.phone
    
    def has_perm(self , perm , obj = None):
        return True
    
    def has_module_perms(self, app_label) :
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    

class OTP(models.Model):
    phone = models.CharField(max_length=11)
    code = models.BigIntegerField()

    def __str__(self) -> str:
        return self.phone
    

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile' , null=True , blank=True)
    avatar = models.ImageField(upload_to='profile/' , default='default_profile/profile.png')

    def __str__(self) -> str:
        return str(self.user)