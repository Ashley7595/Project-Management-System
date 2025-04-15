# Generated by Django 5.1.2 on 2025-04-08 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PM', '0003_task_task_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=20),
        ),
    ]
