# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-20 12:06
from __future__ import unicode_literals

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0001_initial'),
        ('models', '0002_auto_20181216_0720'),
        ('brands', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0002_auto_20180804_1929'),
        ('keepers', '0022_auto_20190619_2232'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserKeeper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iHitStars', core.models.IntegerRangeField(db_index=True, default=0, null=True, verbose_name='hit stars')),
                ('bGetPictures', models.BooleanField(default=False, verbose_name='get description & pictures?')),
                ('tLook4Hits', models.DateTimeField(null=True, verbose_name='assessed interest date/time')),
                ('cWhereCategory', models.CharField(default='title', max_length=10, verbose_name='where category was found')),
                ('bListExclude', models.BooleanField(default=False, verbose_name='exclude from listing?')),
                ('tGotPics', models.DateTimeField(blank=True, null=True, verbose_name='got pictures')),
                ('bAuction', models.BooleanField(default=False, verbose_name='Auction or Auction with Buy It Now')),
                ('tCreate', models.DateTimeField(db_index=True, verbose_name='created on')),
                ('tModify', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('tRetrieved', models.DateTimeField(blank=True, null=True, verbose_name='retrieved info')),
                ('tRetrieveFinal', models.DateTimeField(blank=True, null=True, verbose_name='retrieved info after end')),
                ('iBrand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='brands.Brand', verbose_name='Brand')),
                ('iCategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.Category', verbose_name='Category')),
                ('iItemNumb', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='keepers.Keeper')),
                ('iModel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='models.Model', verbose_name='Model Name/Number')),
                ('iSearch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='searching.Search', verbose_name='Search that first found this item')),
                ('iUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name_plural': 'userkeepers',
                'db_table': 'userkeepers',
            },
        ),
        migrations.AlterUniqueTogether(
            name='userkeeper',
            unique_together=set([('iItemNumb', 'iUser', 'iModel', 'iBrand')]),
        ),
    ]