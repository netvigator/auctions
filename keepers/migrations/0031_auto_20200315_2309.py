# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-03-15 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepers', '0030_auto_20191127_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userkeeper',
            name='bGetPictures',
            field=models.BooleanField(default=False, verbose_name='get pictures?'),
        ),
    ]
