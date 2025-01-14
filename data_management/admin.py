from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from .models import Question, FormSubsection, FormSection, ONAForm

class QuestionAdmin(admin.ModelAdmin):  
   list_display = ("question_id", "description", )
   search_fields = ("question_id", "description", )

class FormSubsectionAdmin(admin.ModelAdmin):
   # form = FormSubsectionAdminForm
   list_display = ("subsection_id", "subsection_title", )
   search_fields = ("subsection_id", "subsection_title", )
   filter_horizontal = ["questions_level1", "questions_level2"]

   

class FormSectionAdmin(admin.ModelAdmin):
   list_display = ("section_id", "section_title", )
   search_fields = ("section_id", "section_title", )
   filter_horizontal = ["form_subsections", "questions_level3"]
    
class ONAFormAdmin(admin.ModelAdmin):
   list_display = ("form_title",)
   filter_horizontal = ["ONA_sections"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(FormSubsection, FormSubsectionAdmin)
admin.site.register(FormSection, FormSectionAdmin)
admin.site.register(ONAForm, ONAFormAdmin)
