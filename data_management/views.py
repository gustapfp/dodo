from django.shortcuts import render
from .forms import EvaluatorForm
from django.views import View
from report.models import ONAFormAnswered
from data_management.models import ONAForm, FormSubsection, FormSection
from django.contrib import messages
from django.shortcuts import redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin



from .helpers.serialize_to_json import serialize_ona_form
from .helpers.views_helper import create_section, verify_evaluator


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
            form.is_valid()
            evaluator = form.save(commit=False)
            

            evaluator = verify_evaluator(
                form_evaluator=evaluator,
                request=request
            )
            ona_form_complete = ONAForm.objects.filter(hospital=request.user.hospital.id).first()
            
            if evaluator.job_role == "001.002" or evaluator.job_role == "000.000": 
                form_id = ona_form_complete.id 
            else:
                subsection = FormSubsection.objects.filter(
                    subsection_id=evaluator.job_role
                ).first()

                section_id = evaluator.job_role[0:3]

                section_complete = ona_form_complete.ONA_sections.filter(
                    section_id=section_id
                ).first()

                section_simplified= FormSection.objects.create(
                    section_id=section_complete.section_id,
                    section_title=section_complete.section_title,

                )
                section_simplified.form_subsections.set([subsection])
                section_simplified.questions_level3.set(section_complete.questions_level3.all())

           


                ona_form_simplified = ONAForm.objects.create(
                    hospital=ona_form_complete.hospital,
                    form_title=ona_form_complete.form_title
                )
                ona_form_simplified.ONA_sections.set([section_simplified])

                form_id = ona_form_simplified.id
                print('---criou---')



     
            return redirect(
                "ona_form",
                form_id= form_id ,
                evaluator_id=evaluator.id
            )
        except Exception as e:
            messages.error(
                request,
                f"Formulário Invalido. Você adicionou informações fora do padrão esperado. Error: {str(e)}",
            )
            return redirect("evaluator_form")


class ONAFormView(LoginRequiredMixin, View):
    template_name = "ONA/ona_form.html"

    def get(self, request, form_id, evaluator_id):
        ona_form = ONAForm.objects.get(id=form_id)

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "ona_json": serialize_ona_form(ona_form),
                "ona_form": ona_form,
            },
        )

    def post(self, request, form_id, evaluator_id):
        ona_form = ONAForm.objects.get(id=form_id)

        form_data = request.POST

   
        new_ona_form = ONAFormAnswered.objects.create(
            ona_form=ona_form, evaluator_id=evaluator_id
        )

        section_list = create_section(
            form_data=form_data, sections=ona_form.ONA_sections.all()
        )

        new_ona_form.answered_sections.set(section_list)

        return redirect("evaluator_form")
