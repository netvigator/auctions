# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-24 08:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_auto_20171124_0635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brandcategory',
            options={'verbose_name_plural': 'brandcategories'},
        ),
        migrations.AlterModelTable(
            name='brandcategory',
            table='brandcategories',
        ),
    ]
