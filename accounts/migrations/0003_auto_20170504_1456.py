# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-04 14:56
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_client_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='passport_number',
            field=models.CharField(error_messages={'unique': 'A client with this passport number already exists.'}, help_text='Required a passport number in the format: LL XXXXXX only.Where L is any letter and X is any number from 0 to 9', max_length=10, unique=True, validators=[accounts.models.PassportNumberValidator()], verbose_name='passport number'),
        ),
    ]
