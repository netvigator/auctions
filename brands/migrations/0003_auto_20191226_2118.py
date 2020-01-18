# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-26 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0002_auto_20191201_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='cLookFor',
            field=models.TextField(blank=True, help_text='Put nick names, common misspellings and alternate brand names here -- leave blank if Bot only needs to look for the brand name.<br>For example, if the brand is Chevrolet, put \'Chevy\' here<br>Each line is evaluated separately, Bot will know item is in this brand if any one line matches.<br/>Bot expands spaces and hyphens,<br/>"Hewlett-Packard" will find Hewlett-Packard, Hewlett Packard and HewlettPackard,<br/>"Hewlett Packard" will find Hewlett Packard, Hewlett-Packard and HewlettPackard', null=True, verbose_name='Considered a hit if this text is found (optional -- if you include, bot will also search for this)'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='cTitle',
            field=models.CharField(db_index=True, help_text='Put the brand name here -- Bot will search for this in the auction title for each item found.<br/>Optionally, you can put additional description in parentheses ().  While searching auction titles, bot will ignore anything in parentheses.<br/>Bot expands spaces and hyphens,<br/>"Hewlett-Packard" will find Hewlett-Packard, Hewlett Packard and HewlettPackard,<br/>"Hewlett Packard" will find Hewlett Packard, Hewlett-Packard and HewlettPackard', max_length=48, verbose_name='brand name'),
        ),
    ]