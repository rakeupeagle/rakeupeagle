# Generated by Django 5.1.1 on 2024-11-06 22:22

import django_fsm
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_alter_recipient_state_alter_team_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-10, 'Archive'), (0, 'New'), (10, 'Current'), (20, 'Closed')], default=0),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-50, 'Archived'), (0, 'New'), (5, 'Invited'), (7, 'Accepted'), (20, 'Confirmed'), (25, 'Assigned'), (30, 'Completed'), (40, 'Declined'), (50, 'Cancelled')], default=0),
        ),
        migrations.AlterField(
            model_name='team',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-50, 'Archived'), (0, 'New'), (5, 'Invited'), (7, 'Accepted'), (20, 'Confirmed'), (25, 'Assigned'), (30, 'Completed'), (40, 'Declined'), (50, 'Cancelled')], default=0),
        ),
    ]