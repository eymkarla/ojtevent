from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


from .managers import UserManager
from .utils import user_media_path


class User(AbstractBaseUser, PermissionsMixin):
    """ user model
    """
    email = models.EmailField(max_length=500, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    image = models.ImageField(upload_to=user_media_path, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name", "last_name")

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def get_short_name(self):
        return f"{self.first_name}"

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".title()

    @property
    def get_display_name(self):
        if self.first_name and self.last_name:
            return self.get_full_name
        return f"{self.email}"
