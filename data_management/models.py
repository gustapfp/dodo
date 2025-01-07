from django.db import models
from django.db.models import ForeignKey
from ..users.models import Sector, Hospital


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
    job_role = models.CharField(max_length=4, choices=JOB_ROLE_CHOICES)
    evaluation_date = models.DateTimeField(auto_now_add=True)
    hospital_sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    email = models.EmailField(max_length=80, unique=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FormQuestions(models.Model):
    question = models.TextField(max_length=1000)
    question_hint = models.CharField(max_length=20)
    question_value = models.IntegerField()
    question_id = models.CharField(max_length=20)
    
    def __str__(self):
        return self.question_id

class FormSubsection(models.Model):
    questions = models.ManyToManyField()

class FormSection(models.Model):
    form_subsections = models.ManyToManyField(FormSubsection, related_name="form_sections") 

class ONAForm(models.Model):
    ONA_sections = models.ManyToManyField(FormSection)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)


