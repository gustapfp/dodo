from django.contrib import admin
from .models import ONAFormAnswered
from .helpers.utils import MetricsCalculator, PowerPointReportGenerator
# Register your models here.


@admin.register(ONAFormAnswered)
class ONAFormansweredAdmin(admin.ModelAdmin):
    list_display = ("ona_form", "evaluator")
    filter_horizontal = ["answered_sections"]
    actions = ["test_admin"]

    @admin.action(description="Criar Relatório")
    def test_admin(self, request, queryset):
        mc = MetricsCalculator()
        # rp = PowerPointReportGenerator()
        for form in queryset:
            metrics_data = mc.get_ona_form_average_distribution(form)
            print(metrics_data)
            print(metrics_data)
            # rp.make_report(data=metrics_data, report_name=form.ona_form.form_title)


# admin.site.register()
