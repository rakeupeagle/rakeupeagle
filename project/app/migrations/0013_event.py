# Generated by Django 3.2.7 on 2021-10-02 12:57

from django.db import migrations, models
import django_fsm
import hashid_field.field


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20211002_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, prefix='', primary_key=True, serialize=False)),
                ('state', django_fsm.FSMIntegerField(choices=[(0, 'New'), (10, 'Active'), (20, 'Archived')], default=0)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, default='', max_length=2000)),
                ('date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, default='', max_length=2000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
