# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-01 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepers', '0013_auto_20180623_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='iGotPictures',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='how many pictures downloaded'),
        ),
    ]
