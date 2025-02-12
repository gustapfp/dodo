from django.contrib import admin
from .models import ONAFormAnswered, ONAFormDistribution
from .helpers.utils import MetricsCalculator, PowerPointReportGenerator
# Register your models here.


@admin.register(ONAFormAnswered)
class ONAFormansweredAdmin(admin.ModelAdmin):
    list_display = ("ona_form", "evaluator")
    filter_horizontal = ["answered_sections"]
    actions = ["make_presentation"]

    @admin.action(description="Criar Relatório")
    def make_presentation(self, request, queryset):
        mc = MetricsCalculator()
        pprp = PowerPointReportGenerator()


        if len(queryset) > 1:
            metrics_data = mc.create_unified_form_metrics(
                ona_form_queryset=queryset
            )
            ona_form = queryset[0].ona_form
            ONAFormDistribution.objects.create(
                ona_form=ona_form,
                distribution_by_subsection=metrics_data["distribution_by_subsection"],
                distribution_by_section=metrics_data["distribution_by_section"],
                ona_answer_total_distribution=metrics_data["ona_answer_total_distribution"],
                score=None,
                hospital=ona_form.hospital,
            )
        else:
            metrics_data = mc.get_ona_form_average_distribution(
                ona_form=queryset[0]
            )

        
             
        
        pprp.make_report(data=metrics_data, report_name=queryset[0].ona_form.form_title)


# admin.site.register()
