from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import EvaluatorForm
from django.views import View
from .models import ONAForm, Evaluator, Hospital
from django.contrib import messages
from django.shortcuts import redirect, HttpResponse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.core import serializers

class EvaluatorView(LoginRequiredMixin, View):
    template_name = "ONA/evaluator_form.html"
    form_class = EvaluatorForm

    def get(self, request):
        form = self.form_class()

        return render(
            request=request,
            template_name=self.template_name,
            context={"form": form}
        )
    
    def post(self, request):
        form = self.form_class(request.POST)
        try:
            form.is_valid()
            evaluator = form.save(commit=False)
            evaluator.hospital = request.user.hospital
            
            evaluator.save()  
            messages.success(request, 'Evaluator successfully created.')
            return redirect("ona_form", hospital_id=request.user.hospital.id)
        except: 
            messages.error(request, f'Formulário Invalido. Você adicionou informações fora do padrão esperado. {form.errors}')
            return redirect('evaluator_form')


class ONAFormView(LoginRequiredMixin, View):
    template_name = "ONA/ona_form.html"
    def get(self, request, hospital_id):
        ona_form = ONAForm.objects.get(hospital=hospital_id)
        
    
        return render(
            request=request,
            template_name=self.template_name,
            context={
                "ona_form": ona_form
                }
        )


         
        

