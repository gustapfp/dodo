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
    active_user = models.BooleanField(default=True)
    sectors = models.ManyToManyField(Sector, related_name='hospital_sectors', on_delete=models.CASCADE)
    last_service = models.DateTimeField(auto_now=True) # TODO: I don't this this is the best way to do this, WE NEED TO find a way to change this field everytime something related to the hospital happerns

    def __str__(self):
        return self.name