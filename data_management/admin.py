from django.contrib import admin

from .models import Question, FormSubsection, FormSection
# Register your models here.
admin.site.register(Question)





class FormSubsectionAdmin(admin.ModelAdmin):
    
   list_display = ("subsection_id", "subsection_title", )
   search_fields = ("subsection_id", "subsection_title", )
   filter_horizontal = ["questions_level1", "questions_level2"]

class FormSectionAdmin(admin.ModelAdmin):
   list_display = ("section_id", "section_title", )
   search_fields = ("section_id", "section_title", )
   filter_horizontal = ["form_subsections", "questions_level3"]
    
admin.site.register(FormSubsection, FormSubsectionAdmin)
admin.site.register(FormSection, FormSectionAdmin)
