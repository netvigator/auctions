# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-03 23:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0009_auto_20191103_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfinder',
            name='bGetPictures',
            field=models.BooleanField(default=False, verbose_name='get description & pictures?'),
        ),
    ]