# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 10:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('markets', '0009_auto_20171217_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ebay_id', models.PositiveSmallIntegerField(verbose_name='ebay condition ID')),
                ('cTitle', models.CharField(max_length=24, verbose_name='ebay condition description')),
            ],
            options={
                'verbose_name_plural': 'conditions',
                'db_table': 'conditions',
            },
        ),
        migrations.CreateModel(
            name='EbayCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ebay_id', models.BigIntegerField(verbose_name='ebay category number')),
                ('ctitle', models.CharField(max_length=48, verbose_name='ebay category description')),
                ('ilevel', models.PositiveSmallIntegerField(verbose_name='level, top is 0, lower levels are bigger numbers')),
                ('bleaf_category', models.BooleanField(verbose_name='leaf category?')),
                ('iTreeVersion', models.PositiveSmallIntegerField(verbose_name='category tree version')),
                ('iMarket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markets.Market', verbose_name='ebay market')),
                ('iparent_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parentcategory', to='ebaycategories.EbayCategory', verbose_name='parent category')),
                ('isupercededby', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supercededby', to='ebaycategories.EbayCategory', verbose_name='superceded by this category')),
            ],
            options={
                'verbose_name_plural': 'ebay categories',
                'db_table': 'ebay categories',
            },
        ),
    ]
