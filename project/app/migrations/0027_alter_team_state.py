# Generated by Django 5.1.1 on 2024-10-03 23:38

import django_fsm
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_remove_recipient_unique_recipient_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-50, 'Archived'), (-30, 'Ignored'), (-20, 'Cancelled'), (-7, 'Declined'), (0, 'New'), (5, 'Invited'), (7, 'Accepted'), (20, 'Confirmed'), (30, 'Completed')], default=0),
        ),
    ]
