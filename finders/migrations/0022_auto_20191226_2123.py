# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-26 21:23
from __future__ import unicode_literals

import core.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0021_auto_20191226_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfinder',
            name='iHitStars',
            field=core.models.IntegerRangeField(default=0, null=True, verbose_name='hit stars (max for item)'),
        ),
    ]