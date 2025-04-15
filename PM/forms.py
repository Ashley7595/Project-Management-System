from django import forms
from app1.models import Project
from .models import Task, EmployeeRoles, EmployeeUser
from datetime import datetime
from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
    input_type = "date"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'task_roles',
            'task_project',
            'task_title',
            'task_description',
            'task_assigned_to',
            'task_priority',
            'task_start_date',
            'task_due_date'
        ]
        widgets = {
            "task_start_date": DateInput(attrs={'class': 'form-control'}),
            "task_due_date": DateInput(attrs={'class': 'form-control'}),
            "task_description": forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            "task_title": forms.TextInput(attrs={'class': 'form-control'}),
            "task_priority": forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            "task_roles": "Roles",
            "task_project": "Project Name",
            "task_title": "Task Name",
            "task_description": "Description",
            "task_assigned_to": "Assigned To",
            "task_priority": "Priority",
            "task_start_date": "Start Date",
            "task_due_date": "Deadline"
        }

        def __init__(self, *args, **kwargs):
            super(TaskForm, self).__init__(*args, **kwargs)

        # Set all fields as not required to remove asterisks
            for field in self.fields.values():
                field.required = False







    def clean_task_start_date(self):
        date_value = self.cleaned_data.get('task_start_date')
        if date_value:
            return date_value  
        raise ValidationError("This field is required.")


    def clean_task_due_date(self):
        date_value = self.cleaned_data.get('task_due_date')
        if not date_value:
            raise ValidationError("This field is required.")
        return date_value




class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_roles', 'task_project', 'task_title', 'task_description', 'task_assigned_to',
                  'task_priority', 'task_start_date', 'task_due_date']
        widgets = {
            "task_start_date": DateInput(), "task_due_date": DateInput(),
            "task_description": forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'style': 'min-height: 100px;'})
        }
        labels = {
            "task_roles": "Roles",
            "task_project": "Project Name",
            "task_title": "Task Name",
            "task_description": "Description",
            "task_assigned_to": "Assigned To",
            "task_priority": "Priority",
            "task_status": "Status",
            'task_start_date': "Start Date",
            "task_due_date": "Deadline"
        }

    def __init__(self, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)

        # Set all fields as not required to remove asterisks
        for field in self.fields.values():
            field.required = False


        roles_to_display = ['Tester', 'Web Developer']
        self.fields['task_roles'].queryset = EmployeeRoles.objects.filter(all_roles__in=roles_to_display)
       