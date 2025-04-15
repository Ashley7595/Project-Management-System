from django import forms
from PM.models import Task
from .models import Bugs

class DateInput(forms.DateInput):
    input_type = "date"



class AddBugsForm(forms.ModelForm):
    class Meta:
        model = Bugs
        fields = ['bug_title', 'bug_description', 'bug_priority', 'bug_severity', 'bug_image', 'bug_date']
        widgets = {
            "bug_date": DateInput(),
            "bug_description": forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'style': 'min-height: 100px;'}),
        }
        labels = {
            "related_task": "Select Task",
            "bug_title": "Bug Title",
            "bug_description": "Description",
            "bug_priority": "Priority",
            "bug_severity": "Severity",       
            "bug_image": "Screenshot",
            "bug_date": "Reported On",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['related_task'].queryset = Task.objects.filter(task_assigned_to=user)
