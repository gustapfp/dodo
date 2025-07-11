from django.db import models
from data_management.models import (
    FormSection,
    FormSubsection,
    ONAForm,
    Question,
    Evaluator,
    Hospital,
)
from pydantic import BaseModel
from django.utils import timezone

class QuestionAnswer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_answers"
    )
    answer = models.CharField(max_length=20, null=True, blank=True)  # For text answers should remove this
    # core = models.BooleanField(default=False)
    comment = models.TextField(max_length=4000, null=True)

    def __str__(self):
        return f"Answer to {self.question.question_id}"


# Create your models here.
class FormSubsectionAnswered(models.Model):
    answered_questions_level_1 = models.ManyToManyField(
        QuestionAnswer, related_name="answered_questions_level_1"
    )
    answered_questions_level_2 = models.ManyToManyField(
        QuestionAnswer, related_name="answered_questions_level_2"
    )
    form_subsection = models.ForeignKey(
        FormSubsection,
        on_delete=models.CASCADE,
        related_name="related_subsection",
        default=None,
    )
    
    def __str__(self):
        return f"Subsection {self.form_subsection.subsection_title}"


class FormSectionAnswered(models.Model):
    answered_subsections = models.ManyToManyField(
        FormSubsectionAnswered, related_name="answered_subsections"
    )
    form_section = models.ForeignKey(
        FormSection,
        on_delete=models.CASCADE,
        related_name="related_section",
        default=None,
    )
    answered_questions_level_3 = models.ManyToManyField(
        QuestionAnswer, related_name="answered_questions_level_3"
    )

    def __str__(self):
        return f"Answered section {self.form_section.section_title}"


class ONAFormAnswered(models.Model):
    answered_sections = models.ManyToManyField(
        FormSectionAnswered, related_name="answered_sections"
    )
    ona_form = models.ForeignKey(
        ONAForm, on_delete=models.CASCADE, related_name="related_ona_form", default=None
    )
    evaluator = models.ForeignKey(
        Evaluator,
        on_delete=models.CASCADE,
        related_name="related_evaluator",
        default=None,
    )
    answered_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Formulário ONA Respondido"
        verbose_name_plural = "Formulários ONA Respondidos"
        
    def __str__(self):
        return f"{self.ona_form.form_title}-respondido por: {self.evaluator.name} - na data: {self.answered_at}"


class AnswerDistribution(BaseModel):
    nao_aplicavel: int
    nao_conforme: int
    parcial_conforme: int
    conforme: int
    supera: int


class SubsectionDistribution(BaseModel):
    subsection_title: str
    subsection_distribution: AnswerDistribution


class SectionDistribution(BaseModel):
    section_title: str
    section_answer_distribution: AnswerDistribution
    answer_distibution_by_subsection: list[SubsectionDistribution]


class ONAMetrics(BaseModel):
    section_distribution: SectionDistribution
    ona_general_answer_distribution: AnswerDistribution


class ONAFormDistribution(models.Model):
    ona_form = models.ForeignKey(
        ONAFormAnswered,
        on_delete=models.CASCADE,
        related_name="related_ona_form_distribution",
        default=None,
    )
    distribution_by_subsection = models.JSONField(default=dict)
    distribution_by_section = models.JSONField(default=dict)
    ona_answer_total_distribution = models.JSONField(default=dict)
    # ona_answer_core_distribution = models.JSONField(default=dict)
    score = models.FloatField(default=0.0, null=True)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="related_hospital_distribution",
        default=None,
    )

    class Meta:
        verbose_name = "Distribuição ONA"
        verbose_name_plural = "Distribuições ONA"
