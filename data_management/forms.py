from django import forms
from .models import Evaluator, Hospital, ONAForm


class EvaluatorForm(forms.ModelForm):
    class Meta:
        model = Evaluator
        fields = "__all__"
        exclude = ('hospital', 'evaluation_date')
        error_messages = {
            'email': {
                'unique': "Esse Email já está em uso. Por favor, preencha o formulário de novo com outro email"
            }
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'Nome',
                'id': 'evaluator-name'
            }),
            'hospital_sector': forms.Select(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'id': 'hospital-sector'
            }),
            'job_role': forms.Select(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'id': 'job-role'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full  p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
                'placeholder': 'nome@email.com',
                'id': 'email-address'
            }),
        }

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

class SubsectionCreationForm(forms.ModelForm):
    pass 