from data_management.models import FormSubsection, FormSection, ONAForm
from django.db.models import QuerySet
import pytz
from django.utils import timezone



class ONAFormAdminHelper:

    def _filter_subsections(self, subsection:FormSubsection, removed_subsections:list[FormSubsection]):
        if subsection in removed_subsections:
            return False
        else:
            return True

    def _copy_a_section(self, obj:FormSection, removed_subsections: QuerySet) -> None:
        """
        Create a clone from the template sectionand filter possible removed_subsectons.
        """
        template_string_index = len(" - TEMPLATE")
        removed_subsections = list(removed_subsections.all())

        subsections_list = list(obj.form_subsections.all())
        filtered_subsections = list(filter(
            lambda subsection: self._filter_subsections(subsection, removed_subsections),
            subsections_list
        ))
        level_3_questions = list(obj.questions_level3.all())

        obj.pk = None
        obj.section_id = obj.section_id
        obj.section_title = obj.section_title[:-template_string_index]
        obj.save()
        obj.form_subsections.set(filtered_subsections)
        obj.questions_level3.set(level_3_questions)


    def make_sections_copys(self, removed_subsections: QuerySet) -> list[FormSection]:
        secao_01 = FormSection.objects.get(section_title='1 SEÇÃO - GESTÃO ORGANIZACIONAL - TEMPLATE')
        self._copy_a_section(secao_01, removed_subsections)

        secao_02 = FormSection.objects.get(section_title='2 SEÇÃO - ATENÇÃO AO PACIENTE - TEMPLATE')
        self._copy_a_section(secao_02, removed_subsections)

        secao_03 = FormSection.objects.get(section_title='3 SEÇÃO - DIAGNÓSTICO E TERAPÊUTICA - TEMPLATE')
        self._copy_a_section(secao_03, removed_subsections)

        secao_04 = FormSection.objects.get(section_title='4 SEÇÃO - GESTÃO DE APOIO - TEMPLATE')
        self._copy_a_section(secao_04, removed_subsections)

        return [secao_01, secao_02, secao_03, secao_04]
    
    def get_current_time_formated_for_title(self):
        saopaulo_tz = pytz.timezone("America/Sao_Paulo")
        date = timezone.now().astimezone(saopaulo_tz)
        #  = datetime.now()
        return f"{date.day}/{date.month}/{date.year}-{date.hour}:{date.minute}"

