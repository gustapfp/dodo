from django import forms
from .models import Evaluator
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from .models import FormSubsection
from django.contrib import admin

class EvaluatorForm(forms.ModelForm):
    class Meta:
        model = Evaluator
        fields = "__all__"
        exclude = ('hospital', 'evaluation_date')