# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-11-27 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0016_auto_20191117_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfoundtemp',
            name='cModelAlphaNum',
            field=models.CharField(max_length=24, null=True, verbose_name='model name/number alpha num only'),
        ),
        migrations.AlterField(
            model_name='itemfound',
            name='iShippingType',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Calculated'), (1, 'Calculated Domestic Flat International'), (2, 'Flat'), (3, 'Flat Domestic Calculated International'), (4, 'Free'), (5, 'Pick Up ONLY!'), (6, 'Freight'), (7, 'Freight Flat'), (8, 'Not Specified'), (9, 'Free Pick Up Option')], null=True, verbose_name='shipping type'),
        ),
    ]
