# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-28 22:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('keepers', '0026_auto_20190621_2159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userkeeper',
            name='tRetrieveFinal',
        ),
        migrations.RemoveField(
            model_name='userkeeper',
            name='tRetrieved',
        ),
    ]
