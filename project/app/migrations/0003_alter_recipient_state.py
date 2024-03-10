# Generated by Django 4.2.7 on 2023-11-15 19:02

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_delete_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipient',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-10, 'Inactive'), (0, 'New'), (10, 'Active')], default=0),
        ),
    ]