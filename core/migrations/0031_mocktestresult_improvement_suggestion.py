# Generated by Django 5.1.6 on 2025-03-13 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='mocktestresult',
            name='improvement_suggestion',
            field=models.TextField(blank=True, null=True),
        ),
    ]
