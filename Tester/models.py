from django.db import models
from app1.models import Project, EmployeeUser, EmployeeRoles
from PM.models import Task  

class Bugs(models.Model):
    related_task = models.ForeignKey('PM.Task', on_delete=models.CASCADE, related_name='bugs')  
    bug_id = models.AutoField(primary_key=True)
    bug_title = models.CharField(max_length=20)
    bug_description = models.TextField()
    bug_priority = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    bug_severity = models.CharField(max_length=50, choices=[('Minor', 'Minor'), ('Major', 'Major'), ('Critical', 'Critical')])
    bug_image = models.ImageField(upload_to='bug_images/', null=True, blank=True)
    is_fixed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    bug_date = models.DateField()

    def __str__(self):
        return self.bug_title
