# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-07 22:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0003_itemfound_ccatheirarchy'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfound',
            name='c2ndCategory',
            field=models.CharField(max_length=48, null=True, verbose_name='secondary category (optional)'),
        ),
        migrations.AddField(
            model_name='itemfound',
            name='i2ndCategoryID',
            field=models.PositiveIntegerField(null=True, verbose_name='secondary category ID (optional)'),
        ),
    ]
