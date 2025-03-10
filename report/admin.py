from django.contrib import admin
from .models import ONAFormAnswered, ONAFormDistribution
from .helpers.utils import MetricsCalculator, PowerPointReportGenerator
from report.helpers.utils import PDFReportGenerator
from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from django.utils import timezone


class ONAFormAdmin(forms.ModelForm):
        from_date = forms.DateField(widget=AdminDateWidget())
        
        class Meta:
            fields = "__all__"





@admin.register(ONAFormAnswered)
class ONAFormansweredAdmin(admin.ModelAdmin):
    list_display = ("ona_form", "evaluator", "answered_at")
    filter_horizontal = ["answered_sections"]
    actions = ["make_presentation", "make_pdf_report"]
    form = ONAFormAdmin
    

    @admin.action(description="Criar Relatório PowerPoint")
    def make_presentation(self, request, queryset):
        mc = MetricsCalculator()
        pprp = PowerPointReportGenerator()
   
        ona_form = queryset[0].ona_form
        if len(queryset) > 1:
            metrics_data = mc.create_unified_form_metrics(
                ona_form_queryset=queryset
            )
            
            ONAFormDistribution.objects.create(
                ona_form=queryset[0],
                distribution_by_subsection=metrics_data["Subsections Distribution"],
                distribution_by_section=metrics_data["Sections Distribution"],
                ona_answer_total_distribution=metrics_data["ONA answer Distribution"],
                score=None,
                hospital=ona_form.hospital,
            )
        else:
            metrics_data = mc.get_ona_form_average_distribution(
                ona_form=queryset[0]
            )     
         
        pprp.make_report(
            data=metrics_data, 
            report_name=queryset[0].ona_form.form_title,
            hospital=ona_form.hospital
            )
   
    @admin.action(description="Enviar Relatório PDF")
    def make_pdf_report(self, request, queryset):
        for report in queryset:
            pdf = PDFReportGenerator(filename=f"Relatório{timezone.now()}",)
            
            pdf.create_pdf_report_for_subsection(
                    evaluator_name=report.evaluator.name,
                    answers=report,
                    evaluator_id=report.evaluator.id
                )


admin.site.register(ONAFormDistribution)
