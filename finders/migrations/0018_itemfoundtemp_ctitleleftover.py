# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-28 01:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0017_auto_20191127_0124'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfoundtemp',
            name='cTitleLeftOver',
            field=models.CharField(max_length=80, null=True, verbose_name='item title less model match'),
        ),
    ]
