from django.db import models
from django.db.models import ForeignKey
from users.models import Hospital, Sector


class Evaluator(models.Model):
    JOB_ROLE_CHOICES = [
        ("MED", "Médico(a)"),
        ("ENF", "Enfermeiro(a)"),
        ("TENF", "Técnico(a) de Enfermagem"),
        ("AENF", "Auxiliar de Enfermagem"),
        ("FARM", "Farmacêutico(a)"),
        ("TFARM", "Técnico(a) de Farmácia"),
        ("FISIO", "Fisioterapeuta"),
        ("TOCUP", "Terapeuta Ocupacional"),
        ("NUTR", "Nutricionista"),
        ("PSI", "Psicólogo(a)"),
        ("ASSOC", "Assistente Social"),
        ("TRAD", "Técnico(a) em Radiologia"),
        ("REC", "Recepcionista"),
        ("SEC", "Secretário(a)"),
        ("ADM", "Administrador(a) Hospitalar"),
        ("CONT", "Contador / Analista Financeiro"),
        ("LIMP", "Auxiliar de Limpeza"),
        ("MAQ", "Maqueiro"),
        ("CENF", "Coordenador(a) de Enfermagem"),
        ("AMB", "Condutor(a) de Ambulância"),
    ]
    name = models.CharField(max_length=80)
    job_role = models.CharField(max_length=5, choices=JOB_ROLE_CHOICES)
    evaluation_date = models.DateTimeField(auto_now_add=True)
    hospital_sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    email = models.EmailField(max_length=80, unique=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_id = models.CharField(max_length=20)
    description = models.TextField(max_length=400, null=True)
    guidance = models.TextField(max_length=400, null=True)
    evidence = models.TextField(max_length=400, null=True)
    # level = models.IntegerField()
    def __str__(self):
        return self.question_id

class FormSubsection(models.Model):
    subsection_id = models.CharField(max_length=20)
    subsection_title = models.CharField(max_length=80)
    questions_level1 = models.ManyToManyField(Question, related_name="level1_questions")
    questions_level2 = models.ManyToManyField(Question, related_name="level2_questions")

    def __str__(self):
        return self.subsection_title

class FormSection(models.Model):
    section_id = models.CharField(max_length=20)
    section_title = models.CharField(max_length=80)
    form_subsections = models.ManyToManyField(FormSubsection, related_name="form_sections") 
    questions_level3= models.ManyToManyField(Question, related_name="level3_questions")

    def __str__(self):
        return self.section_title

class ONAForm(models.Model):
    ONA_sections = models.ManyToManyField(FormSection, related_name="ona_form_sections")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    form_title = models.CharField(max_length=80)

    def __str__(self):
        return self.form_title