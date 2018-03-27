# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-27 09:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebayinfo', '0013_auto_20180327_1634'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ebaycategory',
            old_name='iMarket',
            new_name='iEbaySiteID',
        ),
        migrations.AlterUniqueTogether(
            name='ebaycategory',
            unique_together=set([('iCategoryID', 'iEbaySiteID')]),
        ),
    ]
