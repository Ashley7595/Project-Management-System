from django import forms
from PM.models import Task


class DateInput(forms.DateInput):
    input_type = "date"


# class UpdateTaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['task_project','task_title','task_description','task_priority','task_status']
#         widgets = {
#             "task_due_date": DateInput(),
#             "task_description": forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'style': 'min-height: 100px;'}),
#         }
#         labels = {
#             "task_project": "Project Name",
#             "task_title": "Task",
#             "task_description": "Task Description",
#             "task_priority": "Priority",
#             "task_status": "Status",
#         }
        