# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-17 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0014_auto_20191117_0232'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfound',
            name='iHanglingTime',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='hangling time'),
        ),
    ]
