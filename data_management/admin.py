from django.contrib import admin
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from .forms import HospitalCreationForm, HospitalChangeForm
from .models import Question, FormSubsection, FormSection, ONAForm, Evaluator, Hospital, Sector
from users.models import CustomUser

class QuestionAdmin(admin.ModelAdmin):  
   list_display = ("question_id", "description", )
   search_fields = ("question_id", "description", )

class FormSubsectionAdmin(admin.ModelAdmin):
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



@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    """
    Admin interface for the Hospital model, which links to a CustomUser
    via the 'name' OneToOneField.
    """
  
    add_form = HospitalCreationForm
    form = HospitalChangeForm

    
    fieldsets = (
        (None, {
            "fields": (
                "name",    
                "username",
                "email",
                "contact_number",
                "address",
                "sectors",
                "level",
                "is_active",
            )
        }),
    
    )

   
    list_display = (
        "name",    
        "email",
        "contact_number",
        "is_active",
    )
    list_filter = ("is_active", "sectors",)
    search_fields = ("name", "email",)  
    filter_horizontal = ("sectors",)

    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "username":  
            kwargs["queryset"] = CustomUser.objects.filter(role="hospital")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    
    


admin.site.register(Question, QuestionAdmin)
admin.site.register(FormSubsection, FormSubsectionAdmin)
admin.site.register(FormSection, FormSectionAdmin)
admin.site.register(ONAForm, ONAFormAdmin)
admin.site.register(Evaluator)
admin.site.register(Sector)
