# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-26 21:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0017_auto_20180126_1112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='model',
            old_name='bsplitdigitsok',
            new_name='bSplitDigitsOK',
        ),
    ]
