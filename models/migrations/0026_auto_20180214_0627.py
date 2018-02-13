# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-13 23:27
from __future__ import unicode_literals

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0025_auto_20180130_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='cExcludeIf',
            field=models.TextField(blank=True, help_text='Bot will know item is <b>NOT</b> of this model if any one line matches (each line evaluated separately, put different exclude tests on different lines)', null=True, verbose_name='Not a hit if this text is found (optional)'),
        ),
        migrations.AlterField(
            model_name='model',
            name='cKeyWords',
            field=models.TextField(blank=True, help_text='Optionally, words that must be found in the title <b>IN ADDITION TO</b> model number or name.<br>Put alternate key words on separate lines -- Bot will know item is for this model if words on any one line match.', null=True, verbose_name='model key words (optional)'),
        ),
        migrations.AlterField(
            model_name='model',
            name='cLookFor',
            field=models.TextField(blank=True, help_text='Put nick names, common misspellings and alternate model numbers or names here -- leave blank if Bot only needs to look for the model number or name.<br>Each line is evaluated separately, Bot will know item is in this model if any one line matches.', null=True, verbose_name='Considered a hit if this text is found (optional)'),
        ),
        migrations.AlterField(
            model_name='model',
            name='cTitle',
            field=core.models.gotSomethingOutsideTitleParensCharField(db_index=True, help_text='Put the model number or name here -- Bot will search for this in the auction titles.<br/>Optionally, you can put additional description in parentheses ().  While searching auction titles, bot will ignore anything in parentheses.', max_length=48, verbose_name='model number or name'),
        ),
    ]
