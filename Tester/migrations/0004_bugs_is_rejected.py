# Generated by Django 5.1.2 on 2025-04-10 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tester', '0003_bugs_is_approved_bugs_is_fixed'),
    ]

    operations = [
        migrations.AddField(
            model_name='bugs',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
    ]
