from django.db import models
from django.db.models import ForeignKey
from users.models import CustomUser
from data_management.helpers.consts import JOB_DESCRIPTION_CHOICES

class Sector(models.Model):
    name = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(max_length=80)
    username = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, max_length=80, unique=True
    )
    email = models.EmailField(max_length=80, blank=True)
    contact_number = models.CharField(max_length=16, blank=True)
    address = models.TextField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    sectors = models.ManyToManyField(Sector, related_name="hospital_sectors")
    last_service = models.DateTimeField(
        auto_now=True
    )  # TODO: I don't if this is the best way to do this, WE NEED TO find a way to change this field everytime something related to the hospital happerns

    
    level_choices = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
    ]    
    level = models.IntegerField(default=1, choices=level_choices)

    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitais"

    def __str__(self):
        return self.name


class Evaluator(models.Model):
    name = models.CharField(max_length=150)
    hospital_sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    job_role = models.CharField(max_length=7, choices=JOB_DESCRIPTION_CHOICES)
    evaluation_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=80)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Avaliador"
        verbose_name_plural = "Avaliadores"

    def __str__(self):
        return self.name


class Question(models.Model):
    question_id = models.CharField(max_length=20)
    description = models.TextField(max_length=400, null=True)
    guidance = models.TextField(max_length=400, null=True)
    evidence = models.TextField(max_length=400, null=True)
    core = models.BooleanField(default=False)
    level = models.IntegerField(null=True)

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

    def __str__(self):
        return self.question_id


class FormSubsection(models.Model):
    subsection_id = models.CharField(max_length=20)
    subsection_title = models.CharField(max_length=80)
    questions_level1 = models.ManyToManyField(Question, related_name="level1_questions")
    questions_level2 = models.ManyToManyField(Question, related_name="level2_questions")

    class Meta:
        verbose_name = "Criar Formulário ONA"
        verbose_name_plural = "Criar Formulários ONA"

    def __str__(self):
        return self.subsection_title


class FormSection(models.Model):
    section_id = models.CharField(max_length=20)
    section_title = models.CharField(max_length=80)
    form_subsections = models.ManyToManyField(
        FormSubsection, related_name="form_subsections"
    )
    questions_level3 = models.ManyToManyField(Question, related_name="level3_questions")

    class Meta:
        verbose_name = "Seção"
        verbose_name_plural = "Seções"

    def __str__(self):
        return self.section_title
    

class ONAForm(models.Model):
    ONA_sections = models.ManyToManyField(FormSection, related_name="ona_form_sections", help_text='Selecione as seções que você quer ter no formulário. (A ordem importa!) --- ')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, help_text='Indique o hospital ao qual este formulário está associado.')
    updated_at = models.DateTimeField(auto_now=True)
    form_title = models.CharField(max_length=80, help_text="Titulo para o formulário.")


    class Meta:
        verbose_name = "Formulário ONA para edição"
        verbose_name_plural = "Formulários ONA para edição"

    def __str__(self):
        return self.form_title
