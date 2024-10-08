# Generated by Django 5.1 on 2024-09-13 13:02

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_recipient_user_alter_team_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipient',
            name='name',
            field=models.CharField(blank=True, default='', help_text='Your full name.', max_length=100),
        ),
        migrations.AddField(
            model_name='recipient',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Your mobile number.', max_length=128, null=True, region=None, unique=True),
        ),
        migrations.AddField(
            model_name='team',
            name='name',
            field=models.CharField(blank=True, default='', help_text='Your full name.', max_length=100),
        ),
        migrations.AddField(
            model_name='team',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Your mobile number.', max_length=128, null=True, region=None, unique=True),
        ),
    ]
