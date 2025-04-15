from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import date
from django.conf import settings
import uuid
import datetime
from django.utils import timezone


class EmployeeUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
    

class EmployeeRoles(models.Model):
    employee_roles_choices = (
        ('Tester', 'Tester'),
        ('Web Developer', 'Web Developer'),
        ('Project Manager', 'Project Manager')
    )

    all_roles = models.CharField(max_length=20, choices=employee_roles_choices)

    def __str__(self):
        return self.all_roles



class EmployeeUser(AbstractUser):
    employee_phone = models.CharField(max_length=20, null=True, blank=True, default='')
    employee_roles = models.ForeignKey(EmployeeRoles, related_name='employees', on_delete=models.SET_NULL, null=True, blank=True)
    employee_qualification = models.CharField(max_length=20, null=True, blank=True, default='')
    employee_date = models.DateField(null=True, blank=True, default=None)
    employee_join = models.DateField(default=date.today)
    is_active = models.BooleanField(default=True) 
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.expires_at = timezone.now() + datetime.timedelta(hours=1) 
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() < self.expires_at 

    def __str__(self):
        return f"Token for {self.user.username}"
    

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=50)
    project_manager = models.ForeignKey(EmployeeUser, on_delete=models.SET_NULL, null=True, blank=True)

    project_priority_choices = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    project_priority = models.CharField(max_length=50, choices=project_priority_choices, null=True)
    project_description = models.TextField(null=True)
    project_start_date = models.DateField()
    project_start = models.DateField(auto_now=True)
    project_end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.project_name