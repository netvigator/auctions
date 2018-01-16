# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-16 03:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0008_auto_20180106_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='bAllOfInterest',
            field=models.BooleanField(default=True, help_text='Definitely set to True for desireable & rare brands', verbose_name='want everything from this brand?'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='bWanted',
            field=models.BooleanField(default=True, help_text='Bot will only download full descriptions and pictures if you want', verbose_name='want anything from this brand?'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='cExcludeIf',
            field=models.TextField(blank=True, help_text='Not a hit if this text is found (each line evaluated separately, put different exclude tests on different lines)', null=True, verbose_name='Not a hit if this text is found'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='cLookFor',
            field=models.TextField(blank=True, help_text='Considered a hit if this text is found (each line evaluated separately, put different look for tests on different lines)', null=True, verbose_name='Considered a hit if this text is found'),
        ),
    ]
