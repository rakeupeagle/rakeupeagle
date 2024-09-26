# Generated by Django 5.1.1 on 2024-09-25 23:06

import django_fsm
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_message_is_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-40, 'Blocked'), (-20, 'Cancelled'), (-10, 'Inactive'), (0, 'New'), (5, 'Invited'), (10, 'Active'), (20, 'Confirmed'), (30, 'Assigned')], default=0),
        ),
    ]