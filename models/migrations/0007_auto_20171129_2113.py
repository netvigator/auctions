# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-29 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0006_auto_20171129_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='cexcludeif',
            field=models.TextField(blank=True, null=True, verbose_name='Not a hit if this text is found (each line evaluated separately, put different exclude tests on different lines)'),
        ),
    ]
