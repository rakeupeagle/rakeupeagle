# Generated by Django 3.1.4 on 2020-12-01 19:00

import address.models
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0003_auto_20200830_1851'),
        ('app', '0028_auto_20201201_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipient',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Full Name'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Middle Name'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='recipient',
            name='nick_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Nick Name'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='prefix',
            field=models.CharField(blank=True, max_length=100, verbose_name='Name Prefix'),
        ),
        migrations.AddField(
            model_name='recipient',
            name='suffix',
            field=models.CharField(blank=True, max_length=100, verbose_name='Name Suffix'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='address',
            field=address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.address'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Full Name'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Middle Name'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='nick_name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Nick Name'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='prefix',
            field=models.CharField(blank=True, max_length=100, verbose_name='Name Prefix'),
        ),
        migrations.AddField(
            model_name='volunteer',
            name='suffix',
            field=models.CharField(blank=True, max_length=100, verbose_name='Name Suffix'),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='address',
            field=address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.address'),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='recipient',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]