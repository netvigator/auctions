# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-03 12:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebayinfo', '0015_auto_20180804_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebaycategory',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='ebaycategory',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='ebaycategory',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
