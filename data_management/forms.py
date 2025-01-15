from django import forms
from .models import Evaluator, Hospital
from django.contrib.auth import get_user_model
class EvaluatorForm(forms.ModelForm):
    class Meta:
        model = Evaluator
        fields = "__all__"
        exclude = ('hospital', 'evaluation_date')

class HospitalCreationForm(forms.ModelForm):
    """Form used when creating a new Hospital record in the admin."""
    class Meta:
        model = Hospital
        fields = (
            "name",  
            "username",         # The OneToOneField to CustomUser
            "email",
            "contact_number",
            "address",
            "sectors",
            "level",
            "is_active",
        )
    


class HospitalChangeForm(forms.ModelForm):
    """Form used when editing an existing Hospital record in the admin."""
    class Meta:
        model = Hospital
        fields = (
            "name",
            "username",  
            "email",
            "contact_number",
            "address",
            "sectors",
            "level",
            "is_active",
        )