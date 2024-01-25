from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _


class UserManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("O campo 'username' é necessário!")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("O campo 'is_staff' deve ser True para um superusuário.")
        
        if not extra_fields.get("is_superuser"):
            raise ValueError("O campo 'is_superuser' deve ser True para um superusuário.")

        return self.create_user(username, password, **extra_fields)