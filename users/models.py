from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role="hospital", **extra_fields):
        if not username:
            raise ValueError("CODE user member must have an username address.")
        user = self.model(username=username, role=role, **extra_fields)
        if role == "codemember":
            user.is_staff = True
        else:
            user.is_staff = False

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password, role="codemember", **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("hospital", "Hospital"),
        ("codemember", "Code Member"),
    )

    username = models.CharField(max_length=80, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="hospital")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = "Usuário Customizado"
        verbose_name_plural = "Usuários Customizados"

    def __str__(self):
        return self.username
