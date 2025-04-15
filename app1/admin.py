from django.contrib import admin
from .models import ( EmployeeRoles, EmployeeUser , Project )

# Register your models here.
admin.site.register(EmployeeRoles)
admin.site.register(EmployeeUser)
admin.site.register(Project)
#admin.site.register(Task)


# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('id','task','task_priority','task_description','task_start_date','task_end_date')