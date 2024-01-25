from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

class Detection(models.Model):
    mac_address = models.CharField(max_length=17)
    detection_time = models.DateTimeField()
    object_class = models.CharField(max_length=50)
    image_data = models.ImageField(upload_to='detections/')

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = [ ]

    objects = UserManager()

    def __str__(self):
        return self.username
    
    @property
    def tokens(self):    
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }

class OneTimePassword(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)