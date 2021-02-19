import uuid

from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.gis.db import models


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

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
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

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser

    def save(self, *args, **kwargs):
        # always use a unique id
        self.id = uuid.uuid4()
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
