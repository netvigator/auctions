# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-29 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebaycategories', '0013_auto_20171229_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebaycategory',
            name='iParentID',
            field=models.PositiveIntegerField(default=0, verbose_name='ebay parent category'),
            preserve_default=False,
        ),
    ]
