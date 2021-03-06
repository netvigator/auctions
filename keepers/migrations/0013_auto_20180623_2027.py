# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-23 20:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepers', '0012_auto_20180619_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='bGotPictures',
            field=models.BooleanField(default=False, verbose_name='pictures downloaded?'),
        ),
        migrations.AddField(
            model_name='item',
            name='tGotPictures',
            field=models.DateTimeField(null=True, verbose_name='pictures downloaded'),
        ),
    ]
