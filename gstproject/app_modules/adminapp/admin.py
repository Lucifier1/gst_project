from django.contrib import admin
from app_modules.adminapp import models
from simple_history.admin import SimpleHistoryAdmin
# Register your models here.


class FAQAdmin(SimpleHistoryAdmin):
    list_display = ('question', 'answer','created_at','updated_at')
    search_fields = ('question', 'answer')
    # list_filter = ('history_date', 'history_user')
    
admin.site.register(models.UserVisit)
admin.site.register(models.User)
admin.site.register(models.BasicDetails)
admin.site.register(models.FAQ, FAQAdmin)
admin.site.register(models.Category)
admin.site.register(models.Blog)
admin.site.register(models.Testimonial)
admin.site.register(models.Services)
admin.site.register(models.AboutParameter)

