from django.contrib import admin
from app_modules.userapp import models
from import_export import resources
from import_export.admin import ExportMixin,ImportMixin,ImportExportMixin
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.


# admin.site.register(models.Feedback)

admin.site.register(models.FeedbackResponse,SimpleHistoryAdmin)

admin.site.register(models.ReportFeedback)


class FeedbackResource(resources.ModelResource):
    class Meta:
        model = models.Feedback
        
class FeedbackAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = FeedbackResource 
    list_display = ('from_user','to_user','description','is_active','document','rate')     
    search_fields = ('from_user__username', 'description')
    
    
admin.site.register(models.Feedback, FeedbackAdmin)