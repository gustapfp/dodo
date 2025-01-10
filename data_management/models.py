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
    description = models.CharField(max_length=20)
    guidance = models.TextField(max_length=200, null=True)
    evidence = models.TextField(max_length=200, null=True)
    level = models.IntegerField()
    result = models.IntegerField(default=0)
    
    def __str__(self):
        return self.question_id

class FormSubsection(models.Model):
    level1 = models.ManyToManyField(Question, related_name="level1_questions")
    level2 = models.ManyToManyField(Question, related_name="level2_questions")
    subsection_title = models.CharField(max_length=80)
    subsection_id = models.CharField(max_length=20)
    questions = models.ManyToManyField(Question, related_name="subsections_questions")

class FormSection(models.Model):
    form_subsections = models.ManyToManyField(FormSubsection, related_name="form_sections") 
    level3= models.ManyToManyField(Question, related_name="level3_questions")
    section_id = models.CharField(max_length=20)
    sections_title = models.CharField(max_length=80)

class ONAForm(models.Model):
    ONA_sections = models.ManyToManyField(FormSection, related_name="ona_form_sections")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    form_title = models.CharField(max_length=80)


