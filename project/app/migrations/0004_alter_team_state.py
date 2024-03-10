# Generated by Django 4.2.7 on 2023-11-15 19:03

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_recipient_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-10, 'Inactive'), (0, 'New'), (10, 'Active')], default=0),
        ),
    ]