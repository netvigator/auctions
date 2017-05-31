# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 05:55
from __future__ import unicode_literals

import brands.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cbrandname', models.CharField(db_index=True, max_length=48, verbose_name='brand name')),
                ('bwanted', models.BooleanField(default=True, verbose_name='want anything from this brand?')),
                ('ballofinterest', models.BooleanField(default=True, verbose_name='want everything from this brand?')),
                ('istars', brands.models.IntegerRangeField(verbose_name='desireability, five star brand is most desireable')),
                ('ccomment', models.TextField(null=True, verbose_name='comments')),
                ('cnationality', django_countries.fields.CountryField(max_length=2, null=True)),
                ('cexcludeif', models.TextField(verbose_name='exclude item when this text is found')),
                ('ilegacykey', models.PositiveIntegerField(unique=True, verbose_name='legacy key')),
                ('tlegacycreate', models.DateTimeField(verbose_name='legacy row created on')),
                ('tlegacymodify', models.DateTimeField(verbose_name='legacy row updated on')),
                ('tcreate', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('tmodify', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('iuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'brands',
                'db_table': 'brands',
            },
        ),
    ]
