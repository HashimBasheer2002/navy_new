# Generated by Django 5.1.6 on 2025-03-13 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_mocktestresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobopportunity',
            name='requirements',
            field=models.TextField(default=True),
        ),
    ]
