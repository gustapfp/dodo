from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import EvaluatorForm
from django.views import View
from .models import ONAForm, Evaluator, QuestionAwnser, FormSubsectionAnswered, FormSectionAnswered, ONAFormAnswered
from django.contrib import messages
from django.shortcuts import redirect, HttpResponse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.core import serializers
from .utils import serialize_ona_form

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
            return redirect("ona_form", hospital_id=request.user.hospital.id, evaluator_id=evaluator.id)
        except: 
            messages.error(request, f'Formulário Invalido. Você adicionou informações fora do padrão esperado. {form.errors}')
            return redirect('evaluator_form')


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
                }
        )

    def post(self, request, hospital_id, evaluator_id):
        ona_form = ONAForm.objects.get(hospital=hospital_id)
   
        form_data = request.POST


        new_ona_form = ONAFormAnswered.objects.create(ona_form=ona_form, 
                                                      evaluator_id=evaluator_id
                                                      )
       
    
      

        section_list = []
        for section in ona_form.ONA_sections.all():
            new_section = FormSectionAnswered.objects.create(form_section=section)
            subsection_list = []
            for subsection in section.form_subsections.all():
                new_subsection = FormSubsectionAnswered.objects.create(form_subsection=subsection)

                questions_level_1 = []
                for question in subsection.questions_level1.all():
                    if question.question_id in form_data:
                        answer = form_data.get(question.question_id, None)
                        new_question = QuestionAwnser.objects.create(
                            question=question, 
                            answer=answer
                            )
                        questions_level_1.append(new_question)
                new_subsection.answered_questions_level_1.set(questions_level_1)

                questions_level_2 = []
                for question in subsection.questions_level2.all():
                    if question.question_id in form_data:
                        answer = form_data.get(question.question_id, None)
                        new_question =  QuestionAwnser.objects.create(
                            question=question, 
                            answer=answer
                            )
                        questions_level_2.append(new_question)
                    
                new_subsection.answered_questions_level_2.set(questions_level_1)
                subsection_list.append(new_subsection)

            new_section.answered_subsections.set(subsection_list)


            questions_level_3 = []
            for question in section.questions_level3.all():
                if question.question_id in form_data:
                    answer = form_data.get(question.question_id, None)
                    new_question = QuestionAwnser.objects.create(
                        question=question, 
                        answer=answer
                        )
                    questions_level_3.append(new_question)
            new_section.answered_questions_level_3.set(questions_level_3)
            
            section_list.append(new_section)
      
        new_ona_form.answered_sections.set(section_list)

        return redirect("evaluator_form")

         
        

