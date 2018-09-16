# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-25 21:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepers', '0002_auto_20180426_0420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='dConvertPrice',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price (converted)'),
        ),
        migrations.AlterField(
            model_name='item',
            name='lLocalPrice',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='price (local currency)'),
        ),
    ]
