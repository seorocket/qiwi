from django.contrib import admin
from .models import *

class TaskAdmin(admin.ModelAdmin):
    list_display = ('qiwi_wallet', 'amount', 'status')
    search_fields = ('qiwi_wallet', 'phones')

admin.site.register(Task, TaskAdmin)

class TaskLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'log_entry', 'timestamp')
    search_fields = ('task__qiwi_wallet',)

admin.site.register(TaskLog, TaskLogAdmin)
