# Generated by Django 5.1.2 on 2025-04-09 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_project_is_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='project',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
