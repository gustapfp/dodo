from django.contrib import admin

from .models import Question, FormSubsection, FormSection
# Register your models here.
admin.site.register(Question)

admin.site.register(FormSection)




class FormSubsectionAdmin(admin.ModelAdmin):
    
   list_display = ("subsection_id", "subsection_title", )
   search_fields = ("subsection_id", "subsection_title", )
   filter_horizontal = ["questions_level1", "questions_level2"]

    
admin.site.register(FormSubsection, FormSubsectionAdmin)