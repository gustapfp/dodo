from django.db import models
from django.db.models import ForeignKey


class Evaluator(models.Model):
    name = models.CharField(max_length=80)
    evaluation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
