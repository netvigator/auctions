# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-01 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebayinfo', '0017_auto_20191127_0124'),
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
