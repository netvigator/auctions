# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-15 12:14
from __future__ import unicode_literals

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('brands', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bWant', models.BooleanField(default=True, verbose_name='want this combination?')),
                ('tCreate', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('iBrand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brands.Brand')),
            ],
            options={
                'db_table': 'brandcategories',
                'verbose_name_plural': 'brandcategories',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cTitle', models.CharField(db_index=True, help_text='Put the category name here -- Bot will search for this in the auction titles.<br/>Optionally, you can put additional description in parentheses ().  While searching auction titles, bot will ignore anything in parentheses.', max_length=48, verbose_name='category description')),
                ('cKeyWords', models.TextField(blank=True, help_text='Putting text here is optional, but if there is text here, robot will consider it REQUIRED -- must be found in the title <b>IN ADDITION TO</b> category name.<br>Put alternate key words on separate lines -- Bot will know item is for this category if words on any one line match.', null=True, verbose_name='category key words')),
                ('cLookFor', models.TextField(blank=True, help_text='Put nick names, common misspellings and alternate category names here -- leave blank if Bot only needs to look for the category name.<br>Each line is evaluated separately, Bot will know item is in this category if any one line matches.', null=True, verbose_name='Considered a hit if this text is found (optional)')),
                ('iStars', core.models.IntegerRangeField(default=5, verbose_name='desireability, 10 star category is most desireable')),
                ('bAllOfInterest', models.BooleanField(default=False, help_text='Definitely set to True for desireable & rare categories', verbose_name='want everything of this category?')),
                ('bWantPair', models.BooleanField(default=False, help_text='are you hoping to find these in paris?', verbose_name='prefer pairs?')),
                ('bAccessory', models.BooleanField(default=False, verbose_name='accessory?')),
                ('bComponent', models.BooleanField(default=False, verbose_name='component?')),
                ('cExcludeIf', models.TextField(blank=True, help_text='Bot will know item is <b>NOT</b> of this category if any one line matches (each line evaluated separately, put different exclude tests on different lines)', null=True, verbose_name='Not a hit if this text is found (optional)')),
                ('iLegacyKey', models.PositiveIntegerField(null=True, verbose_name='legacy key')),
                ('iLegacyFamily', models.PositiveIntegerField(null=True, verbose_name='legacy family')),
                ('bModelsShared', models.BooleanField(default=False, help_text='Set to True if different brands use the same model names or numbers in this category', verbose_name='brands share model numbers')),
                ('cRegExLook4Title', models.TextField(null=True)),
                ('cRegExExclude', models.TextField(null=True)),
                ('cRegExKeyWords', models.TextField(null=True)),
                ('tLegacyCreate', models.DateTimeField(null=True, verbose_name='legacy row created on')),
                ('tLegacyModify', models.DateTimeField(null=True, verbose_name='legacy row updated on')),
                ('tCreate', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('tModify', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('iFamily', models.ForeignKey(blank=True, help_text='you can group some categories into families, choose a category to be the lead', null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Category', verbose_name='category family')),
                ('iUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'ordering': ('cTitle',),
                'db_table': 'categories',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.AddField(
            model_name='brandcategory',
            name='iCategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.Category'),
        ),
        migrations.AddField(
            model_name='brandcategory',
            name='iUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('cTitle', 'iUser')]),
        ),
    ]
