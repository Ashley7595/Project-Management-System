from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from .models import EmployeeUser, Project
import re
from datetime import datetime


class DateInput(forms.DateInput):
    input_type = "date"
  


class AddEmployeeForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        label="Confirm Password"
    )

    class Meta:
        model = EmployeeUser
        fields = [
            'first_name', 'last_name', 'username', 'password', 'confirm_password',
            'email', 'employee_qualification','employee_roles','employee_phone',  'employee_date'
        ]
        widgets = {
            'employee_date': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(attrs={'autocomplete': 'new-password'}),

        }
        labels = {
            "first_name": "First Name",  
            "last_name": "Last Name",
            "username": "Username",
            "password": "Password",
            "email": "Email Address",
            "employee_qualification" : "Qualification",
            "employee_roles": "Job Role",
            "employee_phone": "Contact Number",
            "employee_date": "Date of Joining"
        }

    def __init__(self, *args, **kwargs):
        super(AddEmployeeForm, self).__init__(*args, **kwargs)
    
    # Set all fields as required
        for field in self.fields.values():
            field.required = True

        if self.data.get('password'):
            self.fields['password'].widget.attrs['value'] = self.data['password']
        if self.data.get('confirm_password'):
         self.fields['confirm_password'].widget.attrs['value'] = self.data['confirm_password']
    
        self.fields['username'].help_text = None

    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and EmployeeUser.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username


    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            return password
        if EmployeeUser.objects.filter(password=password).exists():
            raise ValidationError("This password is already in use. Please choose another.")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")
        return password
    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

    

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            if EmployeeUser.objects.filter(email=email).exists():
                raise ValidationError("This email is already registered.")
            if not email.endswith("@gmail.com"):
                raise ValidationError("Only Gmail addresses are allowed.")
        return email
    

    def clean_employee_phone(self):
        phone = self.cleaned_data.get("employee_phone")
        if not phone:
            raise ValidationError("Phone number is required.")
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone

    

    def clean_employee_date(self):
        date_value = self.cleaned_data.get('employee_date')
        if date_value:
            return date_value  
        raise ValidationError("This field is required.")



class EditEmployeeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditEmployeeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email is required.")
        if not email.endswith("@gmail.com"): 
            raise ValidationError("Only Gmail addresses are allowed.")
        return email
    

    def clean_employee_phone(self):
        phone = self.cleaned_data.get("employee_phone")
        if not phone:
            raise ValidationError("Phone number is required.")
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")
        return phone
    

    class Meta:
        model = EmployeeUser
        fields = ['first_name', 'last_name', 'email', 'employee_phone', 'employee_roles', 'employee_date']

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "employee_phone": "Contact Number",
            "employee_roles": "Job Role",
            "employee_date": "Date of Joining"
        }



       
class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_manager', 'project_priority', 'project_description',
                  'project_start_date', 'project_end_date']
        widgets = {
            "project_manager": forms.Select(attrs={'class': 'form-control'}),
            "project_description": forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'style': 'min-height: 100px;'}),
            'project_start_date': forms.DateInput(attrs={'type': 'date'}),
            'project_end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            "project_name": "Project Name",
            "project_manager": "Project Manager",
            "project_priority": "Priority",
            "project_description": "Description",
            "project_start_date": "Start Date",
            "project_end_date": "Deadline",
        }

    def __init__(self, *args, **kwargs):
        super(AddProjectForm, self).__init__(*args, **kwargs)
        self.fields['project_manager'].queryset = EmployeeUser.objects.filter(employee_roles__all_roles='Project Manager', is_active=True)
        for field in self.fields.values():
            field.required = True  





class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_manager', 'project_priority', 'project_description',
                  'project_start_date', 'project_end_date']
        widgets = {
            "project_description": forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'style': 'min-height: 100px;'}),
        }
        labels = {
            "project_name": "Project Name",  
            "project_manager": "Project Manager",
            "project_priority": "Priority",
            "project_description": "Description",
            "project_start_date": "Start Date",
            "project_end_date": "Deadline",
        }


    def __init__(self, *args, **kwargs):
        super(EditProjectForm, self).__init__(*args, **kwargs)
        self.fields['project_manager'].queryset = EmployeeUser.objects.filter(employee_roles__all_roles='Project Manager')
        for field in self.fields.values():
            field.required = True  