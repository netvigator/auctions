# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-03 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0010_userfinder_bgetpictures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfinder',
            name='bGetPictures',
            field=models.NullBooleanField(default=False, verbose_name='get description & pictures?'),
        ),
        migrations.AlterField(
            model_name='userfinder',
            name='bListExclude',
            field=models.NullBooleanField(default=False, verbose_name='exclude from listing?'),
        ),
    ]