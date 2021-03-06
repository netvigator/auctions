# Generated by Django 2.2.10 on 2020-05-03 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('finders', '0029_auto_20200328_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemfound',
            name='cLocation',
            field=models.CharField(max_length=58, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='useritemfound',
            name='iSearch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='searching.Search', verbose_name='Search that found this item'),
        ),
    ]
