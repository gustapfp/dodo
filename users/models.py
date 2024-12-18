
from django.contrib.auth.models import AbstractBaseUser



class User(AbstractBaseUser):
    pass
    # is_active = models.BooleanField(
    #     default=False,
    #     help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
    # )
    