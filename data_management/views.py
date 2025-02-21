from django.shortcuts import render
from .forms import EvaluatorForm
from django.views import View
from report.models import ONAFormAnswered
from data_management.models import ONAForm
from django.contrib import messages
from django.shortcuts import redirect, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin



from .helpers.serialize_to_json import serialize_ona_form
from .helpers.views_helper import EvaluatorViewHelper, create_section
from report.helpers.utils import PDFReportGenerator
from django.utils import timezone


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
        helper = EvaluatorViewHelper()
        try:
            form.is_valid()
            evaluator = form.save(commit=False)
            

            evaluator = helper.verify_evaluator(
                form_evaluator=evaluator,
                request=request
            )

            form_id = helper.get_form_id(
                request=request,
                evaluator=evaluator
            )      
            
            return redirect(
                "ona_form",
                form_id= form_id ,
                evaluator_id=evaluator.id
            )
        except Exception as e:
            return HttpResponse(
                f"Formulário Invalido. Você adicionou informações fora do padrão esperado. Error: {str(e)}",
                status=400
            )
            # messages.error(
            #     request,
            #     f"Formulário Invalido. Você adicionou informações fora do padrão esperado. Error: {str(e)}",
            # )
            # return redirect("evaluator_form")


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
        pdf = PDFReportGenerator(filename=f"Relatório do formulário-{evaluator_id}-{timezone.now()}",)
        ona_form = ONAForm.objects.get(id=form_id)

        form_data = request.POST

   
        new_ona_form = ONAFormAnswered.objects.create(
            ona_form=ona_form, evaluator_id=evaluator_id
        )


        section_list = create_section(
            form_data=form_data, sections=ona_form.ONA_sections.all()
        )

        new_ona_form.answered_sections.set(section_list)
        pdf.create_pdf_report_for_subsection(
                evaluator_name=new_ona_form.evaluator.name,
                answers=new_ona_form,
            )
  
        return redirect("evaluator_form")
