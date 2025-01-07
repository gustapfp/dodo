from django.forms import ModelForm
from .models import Evaluator


class EvaluatorForm(ModelForm):
    class Meta:
        model = Evaluator
        fields = ['name', 'job_role', 'evaluation_date', 'hospital_sector', 'email']