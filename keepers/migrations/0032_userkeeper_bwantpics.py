# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-03-18 23:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keepers', '0031_auto_20200315_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='userkeeper',
            name='bWantPics',
            field=models.NullBooleanField(default=False, help_text='By default, Bot will download pictures for all auctions a) with at least one bid, and b) for models with no pictures downloaded yet.  If this is a zero bid auction and you want pictures anyway, chick on this.', verbose_name='Want to download pictures for this?'),
        ),
    ]
