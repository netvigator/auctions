# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-14 22:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0002_auto_20190831_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='iEbayCategory',
            field=models.ForeignKey(blank=True, help_text='Limit search to items listed in this category -- (key words OR ebay category required!) (Both are OK)', null=True, on_delete=django.db.models.deletion.CASCADE, to='ebayinfo.EbayCategory', verbose_name='ebay category (optional)'),
        ),
    ]