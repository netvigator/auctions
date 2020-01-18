# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-01-04 21:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0003_auto_20191226_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='cKeyWords',
            field=models.TextField(blank=True, help_text='Putting text here is optional, but if there is text here, robot will consider it REQUIRED -- must be found in the title <b>IN ADDITION TO</b> brand name.<br>Put alternate key words on separate lines -- Bot will know item is for this brand if words on any one line match.', null=True, verbose_name='category key words'),
        ),
    ]