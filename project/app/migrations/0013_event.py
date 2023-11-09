# Generated by Django 4.2.6 on 2023-11-09 15:05

from django.db import migrations, models
import django_fsm
import hashid_field.field
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_team_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', help_text='Your full name.', max_length=100)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('state', django_fsm.FSMIntegerField(choices=[(-10, 'Archive'), (0, 'New'), (10, 'Current')], default=0)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='', help_text='Please add any other notes you think we should know.', max_length=2000)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('rakedate', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]