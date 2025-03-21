# Generated by Django 5.1.6 on 2025-03-12 07:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_reply_message_remove_reply_sender_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MockTestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=255)),
                ('score', models.IntegerField()),
                ('date_taken', models.DateTimeField(auto_now_add=True)),
                ('veteran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.veteranprofile')),
            ],
        ),
    ]
