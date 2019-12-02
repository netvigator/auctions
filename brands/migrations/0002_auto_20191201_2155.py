# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-12-01 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='cExcludeIf',
            field=models.TextField(blank=True, help_text='Bot will know item is <b>NOT</b> of this brand if any one line matches (each line evaluated separately, put different exclude tests on different lines)<br/>Bot expands spaces and hyphens,<br/>"Hewlett-Packard" will exclude Hewlett-Packard, Hewlett Packard and HewlettPackard,<br/>"Hewlett Packard" will exclude Hewlett Packard, Hewlett-Packard and HewlettPackard', null=True, verbose_name='Not a hit if this text is found (optional)'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='cLookFor',
            field=models.TextField(blank=True, help_text='Put nick names, common misspellings and alternate brand names here -- leave blank if Bot only needs to look for the brand name.<br>Each line is evaluated separately, Bot will know item is in this brand if any one line matches.<br/>Bot expands spaces and hyphens,<br/>"Hewlett-Packard" will find Hewlett-Packard, Hewlett Packard and HewlettPackard,<br/>"Hewlett Packard" will find Hewlett Packard, Hewlett-Packard and HewlettPackard', null=True, verbose_name='Considered a hit if this text is found (optional)'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='cTitle',
            field=models.CharField(db_index=True, help_text='Put the brand name here -- Bot will search for this in the auction titles.<br/>Optionally, you can put additional description in parentheses ().  While searching auction titles, bot will ignore anything in parentheses.<br/>Bot expands spaces and hyphens,<br/>"Hewlett-Packard" will find Hewlett-Packard, Hewlett Packard and HewlettPackard,<br/>"Hewlett Packard" will find Hewlett Packard, Hewlett-Packard and HewlettPackard', max_length=48, verbose_name='brand name'),
        ),
    ]
