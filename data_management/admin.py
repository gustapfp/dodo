from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from .forms import HospitalCreationForm, HospitalChangeForm
from django_object_actions import DjangoObjectActions, action
from .helpers.admin_onaform_helper import ONAFormAdminHelper
import nested_admin

from .models import (
    FormSubsection,
    FormSection,
    ONAForm,
    Evaluator,
    Hospital,
    Sector,
)
from users.models import CustomUser


# class QuestionAdmin(admin.ModelAdmin):
#     list_display = (
#         "question_id",
#         "description",
#     )
#     search_fields = (
#         "question_id",
#         "description",
#     )


class FormSubsectionAdmin(ONAFormAdminHelper, DjangoObjectActions, admin.ModelAdmin):
    
    @action(
        label="Criar Baseado no template", 
        description="Criar Baseado no template com filtros"  # optional
    )
    def create_based_on_template(self, request, queryset):
        ona_template = ONAForm.objects.get(form_title="ONA - TEMPLATE")
        
        sections_list = self.make_sections_copys(removed_subsections=queryset)
 
       
        
        ona_template.pk = None
        date = self.get_current_time_formated_for_title()
        ona_template.form_title = f"Formulario a editar de {date}"
        

        ona_template.save()
        ona_template.ONA_sections.set(sections_list)
        self.message_user(request, "Formulário criado baseado no template com sucesso! Você já pode editar ele agora!")
        
    list_display = (
        "subsection_id",
        "subsection_title",
    )
    search_fields = (
        "subsection_id",
        "subsection_title",
    )
    filter_horizontal = ["questions_level1", "questions_level2"]

    actions = ("create_based_on_template",)
    
    change_actions = ('create_based_on_template',)
    changelist_actions = ('create_based_on_template',)
    
    def has_add_permission(self, request):
        return False 
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class FormSectionAdmin(admin.ModelAdmin):
    list_display = (
        "section_id",
        "section_title",
    )
    search_fields = (
        "section_id",
        "section_title",
    )
    filter_horizontal = ["form_subsections", "questions_level3"]



class ONAFormAdmin(nested_admin.NestedModelAdmin):

    save_as = True
    save_as_continue  = True
    list_display = ("form_title",)
    # filter_horizontal = ["ONA_sections", ]
    # inlines = [ONAInline,]
    fieldsets = (
        (
            "Identificação do Formulário",
          {  
              "fields" : (
                "form_title",
                "hospital",
                
               
            )
          },
        ),
        # (

        #     "Seleção de Seções",
        #     {
        #         "fields" : (
        #         "ONA_sections",
        #     )
        #     }
        # )
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(form_title="ONA TEMPLATE")


    # def save_model(self, request, obj, form, change):
    #     if "save_as_new" in request.POST:
    #         obj.name = f"Copy of {obj.name}"
    # def toolfunc(self, request, obj):
    #     pass
    



   

    



@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    """
    Admin interface for the Hospital model, which links to a CustomUser
    via the 'name' OneToOneField.
    """

    add_form = HospitalCreationForm
    form = HospitalChangeForm

    fieldsets = (
        (
            None,
            {
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
            },
        ),
    )

    list_display = (
        "name",
        "email",
        "contact_number",
        "is_active",
    )
    list_filter = (
        "is_active",
        "sectors",
    )
    search_fields = (
        "name",
        "email",
    )
    filter_horizontal = ("sectors",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "username":
            kwargs["queryset"] = CustomUser.objects.filter(role="hospital")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# admin.site.register(Question, QuestionAdmin)
admin.site.register(FormSubsection, FormSubsectionAdmin)
# admin.site.register(FormSection, FormSectionAdmin)
admin.site.register(ONAForm, ONAFormAdmin)
admin.site.register(Evaluator)
admin.site.register(Sector)
