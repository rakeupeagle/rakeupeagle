# Generated by Django 5.1.1 on 2024-09-26 22:30

import django_fsm
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_message_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-50, 'Archived'), (-30, 'Ignored'), (-20, 'Cancelled'), (-7, 'Declined'), (0, 'New'), (5, 'Invited'), (7, 'Accepted'), (20, 'Confirmed'), (30, 'Completed')], default=0),
        ),
    ]