# Generated by Django 2.2.10 on 2020-04-21 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searching', '0005_search_bgetbuyitnows'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='bInventory',
            field=models.NullBooleanField(default=False, help_text='You may get an avalanche of useless junk if you turn this on -- be careful!', verbose_name="also get 'Store Inventory' (ebay store fixed price items)?"),
        ),
        migrations.AlterField(
            model_name='search',
            name='bGetBuyItNows',
            field=models.NullBooleanField(default=False, help_text='You may get an avalanche of useless junk if you turn this on -- be careful!', verbose_name="also get 'Buy It Nows' (fixed price non auctions)?"),
        ),
    ]
