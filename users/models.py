from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

class CODEMemberManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("CODE user member must have an username address.")
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

class CODEMember(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=80, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CODEMemberManager()
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username

class Sector(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self):
        return self.name
 
class HospitalManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username: 
            raise ValueError("Hospital must have a username, pela provide one. Ex: hospital_paula_ramos")

        hospital = self.model(
            username=username, 
            **extra_fields
        )

        if password:
            hospital.set_password(password)
        hospital.save(using=self._db)


        return hospital 

class Hospital(AbstractBaseUser):
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(max_length=80, blank=True)
    contact_number = models.CharField(max_length=16, blank=True)
    address = models.TextField(max_length=150, blank=True)
    is_active  = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False) 
    sectors = models.ManyToManyField(Sector, related_name='hospital_sectors')
    last_service = models.DateTimeField(auto_now=True) # TODO: I don't this this is the best way to do this, WE NEED TO find a way to change this field everytime something related to the hospital happerns

    objects = HospitalManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        self.last_service = now()
        
# Signals for updating last_service
@receiver(m2m_changed, sender=Hospital.sectors.through)
def update_last_service_on_sectors_change(sender, instance, **kwargs):
    instance.last_service = now()
    instance.save()


