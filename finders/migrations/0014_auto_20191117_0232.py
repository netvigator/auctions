# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-11-17 02:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0013_itemfoundtemp_cfoundmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemfound',
            name='dBuyItNowPrice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='buy it now price (converted to USD)'),
        ),
        migrations.AddField(
            model_name='itemfound',
            name='lBuyItNowPrice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='buy it now price'),
        ),
        migrations.AlterField(
            model_name='useritemfound',
            name='iModel',
            field=models.ForeignKey(blank=True, help_text='You can display models for a particular brand by changing to that brand (just below), hit save, then edit again', null=True, on_delete=django.db.models.deletion.CASCADE, to='models.Model', verbose_name='Model Name/Number'),
        ),
    ]
