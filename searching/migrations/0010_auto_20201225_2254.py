# Generated by Django 3.1.4 on 2020-12-25 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0009_auto_20200621_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='bGetBuyItNows',
            field=models.BooleanField(blank=True, default=False, help_text='You may get an avalanche of useless junk if you turn this on -- be careful!', null=True, verbose_name="also get 'Buy It Nows' (fixed price non auctions)?"),
        ),
        migrations.AlterField(
            model_name='search',
            name='bInventory',
            field=models.BooleanField(blank=True, default=False, help_text='You may get an avalanche of useless junk if you turn this on -- be careful!', null=True, verbose_name="also get 'Store Inventory' (fixed price items in ebay stores)?"),
        ),
    ]