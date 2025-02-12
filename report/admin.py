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
        mc_data1 = mc.get_ona_form_average_distribution(queryset[1])
        mc_data0 = mc.get_ona_form_average_distribution(queryset[0])
        form = mc.create_unified_form(ona_form_queryset=queryset)
        
        # metrics_data = mc.get_ona_form_average_distribution(form)
        print("--------------------")
        print(mc_data1["Subsections Distribution"])
        print("--------------------")
        print(mc_data0["Subsections Distribution"])
        print("--------------------")
        print(form)
        print("--------------------")
        # rp.make_report(data=metrics_data, report_name=form.ona_form.form_title)


# admin.site.register()
