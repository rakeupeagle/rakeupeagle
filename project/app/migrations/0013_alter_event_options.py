# Generated by Django 5.1.1 on 2024-09-15 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_message_sid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-year',)},
        ),
    ]