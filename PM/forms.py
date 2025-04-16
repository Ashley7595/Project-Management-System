from django import forms
from app1.models import Project, EmployeeRoles, EmployeeUser
from .models import Task
from datetime import datetime
from django.core.exceptions import ValidationError


class DateInput(forms.DateInput):
    input_type = "date"


class TaskForm(forms.ModelForm):
    # Move this outside the Meta class!
    task_roles = forms.ModelChoiceField(
        queryset=EmployeeRoles.objects.all(),
        empty_label="Select a Role",
        widget=forms.Select(attrs={'class': 'form-control'})  # This ensures it's rendered as a dropdown
    )

    class Meta:
        model = Task
        fields = [
            'task_project', 'task_title', 'task_description', 'task_roles',
            'task_assigned_to', 'task_priority', 'task_status', 'task_due_date'
        ]
        widgets = {
            "task_start_date": DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "task_due_date": DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            "task_description": forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'style': 'min-height: 100px;'
            }),
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
        task_roles = forms.ModelChoiceField(
        queryset=EmployeeRoles.objects.exclude(all_roles='Project Manager'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
        label="Roles"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        # Filter roles to only show 'Tester' and 'Web Developer'
        roles_to_display = ['Tester', 'Web Developer']
        self.fields['task_roles'].queryset = EmployeeRoles.objects.filter(all_roles__in=roles_to_display)

        # Filter project list based on logged-in user
        if user:
            self.fields['task_project'].queryset = Project.objects.filter(project_manager=user)
            # Add this after filtering project
            self.fields['task_assigned_to'].queryset = EmployeeUser.objects.none()


        # Add class to other fields if needed
        for field_name in self.fields:
            if field_name != 'task_description':  # Already styled above
                self.fields[field_name].widget.attrs.setdefault('class', 'form-control')


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
       