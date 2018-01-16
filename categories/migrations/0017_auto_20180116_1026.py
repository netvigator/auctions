# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-16 03:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0016_category_bmodelsshared'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='bAllOfInterest',
            field=models.BooleanField(default=False, help_text='Definitely set to True for desireable & rare categories', verbose_name='want everything of this category?'),
        ),
        migrations.AlterField(
            model_name='category',
            name='bKeyWordRequired',
            field=models.BooleanField(default=False, help_text='Bot will know this model is for sale only if these key words are in the description', verbose_name='key word required?'),
        ),
        migrations.AlterField(
            model_name='category',
            name='bModelsShared',
            field=models.BooleanField(default=False, help_text='Set to True if different brands use the same model names or numbers in this category', verbose_name='brands share model numbers'),
        ),
        migrations.AlterField(
            model_name='category',
            name='bWantPair',
            field=models.BooleanField(default=False, help_text='are you hoping to find these in paris?', verbose_name='only want pairs?'),
        ),
        migrations.AlterField(
            model_name='category',
            name='cExcludeIf',
            field=models.TextField(blank=True, help_text='Not a hit if this text is found (each line evaluated separately, put different exclude tests on different lines)', null=True, verbose_name='Not a hit if this text is found'),
        ),
        migrations.AlterField(
            model_name='category',
            name='cKeyWords',
            field=models.CharField(blank=True, help_text='Bot will look for this text in the item description', max_length=88, null=True, verbose_name='category key words'),
        ),
        migrations.AlterField(
            model_name='category',
            name='cLookFor',
            field=models.TextField(blank=True, help_text='Considered a hit if this text is found -- each line evaluated separately, put different look for tests on different lines', null=True, verbose_name='Considered a hit if this text is found'),
        ),
        migrations.AlterField(
            model_name='category',
            name='iFamily',
            field=models.ForeignKey(blank=True, help_text='you can group some categories into families, choose a category to be the lead', null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Category', verbose_name='category family'),
        ),
    ]
