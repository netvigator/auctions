# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-27 23:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0017_itemfoundtemp_ifoundmodellen'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfound',
            name='cSubTitle',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='item sub title'),
        ),
    ]
