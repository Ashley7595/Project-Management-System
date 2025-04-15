from django.db import models
from app1.models import Project, EmployeeUser, EmployeeRoles

class Task(models.Model):
    task_title = models.CharField(max_length=255)
    task_description = models.TextField()
    task_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    task_roles = models.ManyToManyField(EmployeeRoles, related_name='tasks_roles') 
    task_assigned_to = models.ForeignKey(EmployeeUser, on_delete=models.CASCADE, related_name='assigned_tasks', null=True,          # <-- allows NULL in the database
    blank=True)
    task_priority = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    task_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    task_start_date = models.DateField(null=True)
    task_due_date = models.DateField()

    def __str__(self):
        return self.task_title