from django.db import models
from django.db.models import ForeignKey
from users.models import CustomUser

class Sector(models.Model):
    name = models.CharField(max_length=80, unique=True)
    def __str__(self):
        return self.name
 
class Hospital(models.Model):
    name = models.CharField(max_length=80)
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, max_length=80, unique=True)
    email = models.EmailField(max_length=80, blank=True)
    contact_number = models.CharField(max_length=16, blank=True)
    address = models.TextField(max_length=150, blank=True)
    is_active  = models.BooleanField(default=True)
    sectors = models.ManyToManyField(Sector, related_name='hospital_sectors')
    last_service = models.DateTimeField(auto_now=True) # TODO: I don't this this is the best way to do this, WE NEED TO find a way to change this field everytime something related to the hospital happerns
    level = models.IntegerField(default=1)


    def __str__(self):
        return self.name


class Evaluator(models.Model):
    JOB_ROLE_CHOICES = [
        (None, "Escolha sua profissão..."),
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
    name = models.CharField(max_length=150)
    hospital_sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    job_role = models.CharField(max_length=5, choices=JOB_ROLE_CHOICES)
    evaluation_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=80, unique=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Question(models.Model):
    question_id = models.CharField(max_length=20)
    description = models.TextField(max_length=400, null=True)
    guidance = models.TextField(max_length=400, null=True)
    evidence = models.TextField(max_length=400, null=True)
 
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
    

class QuestionAwnser(models.Model):
    ona_form = models.ForeignKey(ONAForm, on_delete=models.CASCADE, related_name="form_answers")
    form_subsection = models.ForeignKey(FormSubsection, on_delete=models.CASCADE, related_name="form_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_answers")
    answer = models.IntegerField(null=True, blank=True)  # For text answers
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.question_id} in {self.ona_form.form_title}"
    
class FormSubsectionAnswered(models.Model):
    answered_questions = models.ManyToManyField(QuestionAwnser, related_name="answered_questions")

class FormSectionAnswered(models.Model):
    answered_subsections = models.ManyToManyField(QuestionAwnser, related_name="answered_subsections")
    
class ONAFormAnswered(models.Model):
    answered_sections = models.ManyToManyField(QuestionAwnser, related_name="answered_sections")
