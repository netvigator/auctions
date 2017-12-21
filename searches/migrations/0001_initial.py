# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-21 10:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ebaycategories', '0008_auto_20171221_1516'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cKeyWords', models.CharField(max_length=98, verbose_name='search for key words')),
                ('tCreate', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('tModify', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('iEbayCategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ebaycategories.EbayCategory', verbose_name='ebay category (optional)')),
                ('iUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name_plural': 'searches',
                'db_table': 'searches',
            },
        ),
        migrations.AlterUniqueTogether(
            name='search',
            unique_together=set([('cKeyWords', 'iEbayCategory')]),
        ),
    ]
