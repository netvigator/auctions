# Generated by Django 3.1.4 on 2020-12-25 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebayinfo', '0019_auto_20191214_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='bHasCategories',
            field=models.BooleanField(null=True, verbose_name='has own categories?'),
        ),
    ]