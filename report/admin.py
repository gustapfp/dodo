from django.contrib import admin
from .models import ONAFormAnswered
from .helpers.utils import MetricsCalculator, ReportGenerator
# Register your models here.

    
@admin.register(ONAFormAnswered)
class ONAFormansweredAdmin(admin.ModelAdmin):
   list_display = ("ona_form", "evaluator")
   filter_horizontal = ["answered_sections"]
   actions = ['test_admin']

    
   @admin.action(description="Test admin action")
   def test_admin(self,request, queryset):
      mc = MetricsCalculator()
      rp = ReportGenerator()
      for form in queryset:
         metrics_data = mc.get_ona_form_average_distribution(form)
         rp.make_report(
            data=metrics_data,
            report_name=form.ona_form.form_title
         )


# admin.site.register()