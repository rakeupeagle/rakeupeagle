# Generated by Django 5.1.1 on 2024-10-24 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_rename_admin_notes_assignment_notes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='public_notes',
        ),
        migrations.RemoveField(
            model_name='recipient',
            name='public_notes',
        ),
        migrations.RemoveField(
            model_name='team',
            name='public_notes',
        ),
    ]
