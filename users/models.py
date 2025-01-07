from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class User(AbstractBaseUser):
    pass
    # is_active = models.BooleanField(
    #     default=False,
    #     help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
    # )


class Sector(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=80, unique=True)
    email = models.EmailField(max_length=80)
    contact_number = models.TextField(max_length=16)
    address = models.TextField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    active_user = models.BooleanField(default=True)
    sectors = models.ManyToManyField(Sector, related_name='Hospitals', on_delete=models.CASCADE)
    # last_service = models.ForeignKey

    def __str__(self):
        return self.name