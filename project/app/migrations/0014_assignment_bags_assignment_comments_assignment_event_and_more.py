# Generated by Django 4.2.6 on 2023-11-09 15:11

from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='bags',
            field=models.IntegerField(blank=True, help_text='Actual Bags Used', null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='comments',
            field=models.TextField(blank=True, default='', help_text='Please add any other notes you think we should know.', max_length=2000),
        ),
        migrations.AddField(
            model_name='assignment',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='app.event'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='hours',
            field=models.FloatField(blank=True, help_text='Actual Hours Worked', null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='notes',
            field=models.TextField(blank=True, default='', help_text='Internal (private) notes.', max_length=2000),
        ),
        migrations.AddField(
            model_name='assignment',
            name='recipient_state',
            field=django_fsm.FSMIntegerField(choices=[(-40, 'Blocked'), (-30, 'Archived'), (-20, 'Cancelled'), (-10, 'Excluded'), (0, 'New'), (10, 'Included'), (20, 'Confirmed'), (30, 'Checked-In'), (40, 'Missed'), (50, 'Complete')], default=0),
        ),
        migrations.AddField(
            model_name='assignment',
            name='team_state',
            field=django_fsm.FSMIntegerField(choices=[(-30, 'Archived'), (-20, 'Cancelled'), (-10, 'Excluded'), (0, 'New'), (10, 'Included'), (20, 'Confirmed'), (30, 'Checked-In'), (40, 'Missed'), (50, 'Complete')], default=0),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='state',
            field=django_fsm.FSMIntegerField(choices=[(-40, 'Blocked'), (-30, 'Archived'), (-20, 'Cancelled'), (-10, 'Excluded'), (0, 'New'), (10, 'Included'), (20, 'Confirmed'), (30, 'Checked-In'), (40, 'Missed'), (50, 'Complete')], default=0),
        ),
    ]