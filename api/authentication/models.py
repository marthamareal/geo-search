import uuid
from datetime import datetime, timedelta

import jwt
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.gis.db import models

from api.geosearch.settings import SECRET_KEY


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class GeoUser(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    email = models.EmailField(max_length=100, unique=True, db_index=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """
        Returns a string representation of `User`.
        """
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        payload = {
            "id": str(self.id),
            "email": self.email,
            "exp": datetime.now() + timedelta(days=1)
        }
        return jwt.encode(payload, SECRET_KEY).decode('utf-8')

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser

