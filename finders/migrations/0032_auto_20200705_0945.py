# Generated by Django 2.2.13 on 2020-07-05 09:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0031_itemfoundtemp_bmodelkeywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useritemfound',
            name='tCreate',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='created on'),
        ),
    ]
