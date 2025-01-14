from django.contrib import admin
from .models import Question, FormSubsection, FormSection
# Register your models here.
admin.site.register(Question)
admin.site.register(FormSubsection)
admin.site.register(FormSection)