from django.db import models
from django.db.models import ForeignKey


# class Hospital(models.Model):
#     name = models.CharField(max_length=80)
#     address = models.CharField(max_length=80)
#     phone = models.CharField(max_length=80)
#     email = models.EmailField(max_length=80)
#     description = models.TextField()

# class HospitalSector(models):
#     hospital = ForeignKey(Hospital)

# # Create your models here.
# class Sorting(models.Model):

#     hospitals = Hospital.objects.all()
#     hospital_choices = [hospital.name for hospital in hospitals]

#     hospital = models.CharField(
#         max_length=80, 
#         choices=hospital_choices
#         )