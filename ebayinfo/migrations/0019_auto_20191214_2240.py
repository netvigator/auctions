# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-14 22:40
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ebayinfo', '0018_auto_20191201_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebaycategory',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to='ebayinfo.EbayCategory'),
        ),
    ]
