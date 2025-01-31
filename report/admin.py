from django.contrib import admin
from .models import ONAFormAnswered
from .helpers.utils import MetricsCalculator
# Register your models here.

    
@admin.register(ONAFormAnswered)
class ONAFormansweredAdmin(admin.ModelAdmin):
   list_display = ("ona_form", "evaluator")
   filter_horizontal = ["answered_sections"]
   actions = ['test_admin']

    
   @admin.action(description="Test admin action")
   def test_admin(self,request, queryset):
      mc = MetricsCalculator()
      for form in queryset:
         mc.get_ona_form_average_distribution(form)
      

# admin.site.register()