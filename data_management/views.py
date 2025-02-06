from django.shortcuts import render
from .forms import EvaluatorForm
from django.views import View
from report.models import ONAForm, ONAFormAnswered
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from data_management.models import Evaluator


from .helpers.serialize_to_json import serialize_ona_form
from .helpers.answers_organizer import create_section


class EvaluatorView(LoginRequiredMixin, View):
    template_name = "ONA/evaluator_form.html"
    form_class = EvaluatorForm

    def get(self, request):
        form = self.form_class()

        return render(
            request=request, template_name=self.template_name, context={"form": form}
        )

    def post(self, request):
        form = self.form_class(request.POST)
        try:
            # form.is_valid()
            evaluator = form.save(commit=False)
            db_evaluator =  Evaluator.objects.filter(email=evaluator.email).first()

            if  db_evaluator:
                evaluator = db_evaluator

                messages.success(request, "Bem vindo de volta!")
            else:
                evaluator.hospital = request.user.hospital
                evaluator.save()
                messages.success(request, "Avaliador cadastrado com sucesso")
                

            return redirect(
                "ona_form",
                hospital_id=request.user.hospital.id,
                evaluator_id=evaluator.id,
            )
        except:
            messages.error(
                request,
                f"Formulário Invalido. Você adicionou informações fora do padrão esperado. {form.errors}",
            )
            return redirect("evaluator_form")


class ONAFormView(LoginRequiredMixin, View):
    template_name = "ONA/ona_form.html"

    def get(self, request, hospital_id, evaluator_id):
        ona_form = ONAForm.objects.get(hospital=hospital_id)

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "ona_json": serialize_ona_form(ona_form),
                "ona_form": ona_form,
            },
        )

    def post(self, request, hospital_id, evaluator_id):
        ona_form = ONAForm.objects.get(hospital=hospital_id)

        form_data = request.POST

        print(form_data)

        new_ona_form = ONAFormAnswered.objects.create(
            ona_form=ona_form, evaluator_id=evaluator_id
        )

        section_list = create_section(
            form_data=form_data, sections=ona_form.ONA_sections.all()
        )

        new_ona_form.answered_sections.set(section_list)

        return redirect("evaluator_form")
