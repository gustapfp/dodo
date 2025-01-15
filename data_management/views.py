from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import EvaluatorForm
from django.views import View
from .models import ONAForm, Evaluator
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

class OnaFormView(TemplateView):
    template_name = "ONA/ona_form.html"


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
        if form.is_valid():
            evaluator = form.save(commit=False)
            evaluator.hospital = request.user.hospital
            evaluator.save()  
            messages.success(request, 'Evaluator successfully created.')
            return redirect("ona_form")
        else: 
            messages.error(request, 'Formulário Invalido. Você adicionou informações fora do padrão esperado.')
            return redirect('evaluator_form')
