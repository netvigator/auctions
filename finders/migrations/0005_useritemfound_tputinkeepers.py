# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-28 22:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0004_remove_useritemfound_tgotpics'),
    ]

    operations = [
        migrations.AddField(
            model_name='useritemfound',
            name='tPutInKeepers',
            field=models.DateTimeField(blank=True, null=True, verbose_name='User has Keeper row'),
        ),
    ]