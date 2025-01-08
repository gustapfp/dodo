from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CODEMemberManeger(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("CODE user member must have an email address.")
        user = self.model(
            email=self.normalize_email(email=email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.save(usign=self._db)

class CODEMember(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email_adress", max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CODEMemberManeger()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Sector(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self):
        return self.name
 
class HospitalManager(BaseUserManager):
    def crete_user(self, username, password=None, **extra_fields):
        if not username: 
            raise ValueError("Hospital must have a username, pela provide one. Ex: hospital_paula_ramos")
        
        hospital = self.model(
            username=username, 
            **extra_fields
        )
        if password:
            hospital.set_password(password)
        hospital.save(usign=self._db)
        return hospital 

class Hospital(AbstractBaseUser):
    username = models.CharField(max_length=80, unique=True)
    email = models.EmailField(max_length=80, blank=True)
    contact_number = models.CharField(max_length=16, blank=True)
    address = models.TextField(max_length=150, blank=True)
    is_active  = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    sectors = models.ManyToManyField(Sector, related_name='hospital_sectors')
    last_service = models.DateTimeField(auto_now=True) # TODO: I don't this this is the best way to do this, WE NEED TO find a way to change this field everytime something related to the hospital happerns

    objects = HospitalManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'sectors']



    def __str__(self):
        return self.username