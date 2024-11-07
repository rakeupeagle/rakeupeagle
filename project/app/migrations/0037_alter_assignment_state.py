# Generated by Django 5.1.1 on 2024-11-07 02:46

import django_fsm
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_event_unique_event_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-10, 'Archive'), (0, 'New'), (10, 'Current'), (20, 'Closed')], default=0),
        ),
    ]
