# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-01-26 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepers', '0017_auto_20190114_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keeper',
            name='iFeedbackScore',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='seller feedback score'),
        ),
    ]
