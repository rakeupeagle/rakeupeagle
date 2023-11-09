# Generated by Django 4.2.6 on 2023-11-09 20:16

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_recipient_state_alter_team_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yard',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-20, 'Cancelled'), (-10, 'Excluded'), (0, 'New'), (10, 'Included'), (20, 'Confirmed')], default=0),
        ),
    ]
