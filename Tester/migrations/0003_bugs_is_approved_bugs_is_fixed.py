# Generated by Django 5.1.2 on 2025-04-10 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tester', '0002_alter_bugs_bug_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='bugs',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bugs',
            name='is_fixed',
            field=models.BooleanField(default=False),
        ),
    ]
