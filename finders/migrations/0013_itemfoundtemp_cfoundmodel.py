# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-10 02:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0012_auto_20191107_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfoundtemp',
            name='cFoundModel',
            field=models.CharField(max_length=24, null=True, verbose_name='model name/number found in auction title'),
        ),
    ]
