# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-19 10:11
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('itemhits', '0004_auto_20171219_1542'),
    ]

    operations = [
        migrations.RenameField(
            model_name='itemhit',
            old_name='imodel',
            new_name='iModel',
        ),
        migrations.RemoveField(
            model_name='itemhit',
            name='cbuyitnow',
        ),
        migrations.RemoveField(
            model_name='itemhit',
            name='clastbid',
        ),
        migrations.RemoveField(
            model_name='itemhit',
            name='mBuyItNow',
        ),
        migrations.RemoveField(
            model_name='itemhit',
            name='mBuyItNow_currency',
        ),
        migrations.RemoveField(
            model_name='itemhit',
            name='mLastBid',
        ),
        migrations.RemoveField(
            model_name='itemhit',
            name='mLastBid_currency',
        ),
        migrations.RemoveField(
            model_name='itemhit',
            name='tAuctionBeg',
        ),
        migrations.RemoveField(
            model_name='itemhit',
            name='tAuctionEnd',
        ),
        migrations.AddField(
            model_name='itemhit',
            name='bBestOfferable',
            field=models.BooleanField(default=False, verbose_name='best offer enabled?'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='bBuyItNowable',
            field=models.BooleanField(default=False, verbose_name='buy it now enabled?'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='cCategory',
            field=models.CharField(max_length=48, null=True, verbose_name='primary category'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='cCondition',
            field=models.CharField(max_length=28, null=True, verbose_name='condition display name'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='cCountry',
            field=django_countries.fields.CountryField(max_length=2, null=True, verbose_name='country'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='cEbayItemURL',
            field=models.CharField(max_length=188, null=True, verbose_name='ebay item URL'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='cGalleryURL',
            field=models.CharField(max_length=88, null=True, verbose_name='gallery pic URL'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='cLocation',
            field=models.CharField(max_length=48, null=True, verbose_name='location'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='cMarket',
            field=models.CharField(max_length=14, null=True, verbose_name='market Global ID'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='cSellingState',
            field=models.CharField(max_length=18, null=True, verbose_name='selling state'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='iCategoryID',
            field=models.IntegerField(null=True, verbose_name='primary category ID'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='iConditionID',
            field=models.IntegerField(null=True, verbose_name='condition ID'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='mCurrentPrice',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=None, default_currency='USD', max_digits=10, null=True, verbose_name='current price (local currency)'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='mCurrentPrice_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('XUA', 'ADB Unit of Account'), ('AFN', 'Afghani'), ('DZD', 'Algerian Dinar'), ('ARS', 'Argentine Peso'), ('AMD', 'Armenian Dram'), ('AWG', 'Aruban Guilder'), ('AUD', 'Australian Dollar'), ('AZN', 'Azerbaijanian Manat'), ('BSD', 'Bahamian Dollar'), ('BHD', 'Bahraini Dinar'), ('THB', 'Baht'), ('PAB', 'Balboa'), ('BBD', 'Barbados Dollar'), ('BYN', 'Belarussian Ruble'), ('BYR', 'Belarussian Ruble'), ('BZD', 'Belize Dollar'), ('BMD', 'Bermudian Dollar (customarily known as Bermuda Dollar)'), ('BTN', 'Bhutanese ngultrum'), ('VEF', 'Bolivar Fuerte'), ('BOB', 'Boliviano'), ('XBA', 'Bond Markets Units European Composite Unit (EURCO)'), ('BRL', 'Brazilian Real'), ('BND', 'Brunei Dollar'), ('BGN', 'Bulgarian Lev'), ('BIF', 'Burundi Franc'), ('XOF', 'CFA Franc BCEAO'), ('XAF', 'CFA franc BEAC'), ('XPF', 'CFP Franc'), ('CAD', 'Canadian Dollar'), ('CVE', 'Cape Verde Escudo'), ('KYD', 'Cayman Islands Dollar'), ('CLP', 'Chilean peso'), ('XTS', 'Codes specifically reserved for testing purposes'), ('COP', 'Colombian peso'), ('KMF', 'Comoro Franc'), ('CDF', 'Congolese franc'), ('BAM', 'Convertible Marks'), ('NIO', 'Cordoba Oro'), ('CRC', 'Costa Rican Colon'), ('HRK', 'Croatian Kuna'), ('CUP', 'Cuban Peso'), ('CUC', 'Cuban convertible peso'), ('CZK', 'Czech Koruna'), ('GMD', 'Dalasi'), ('DKK', 'Danish Krone'), ('MKD', 'Denar'), ('DJF', 'Djibouti Franc'), ('STD', 'Dobra'), ('DOP', 'Dominican Peso'), ('VND', 'Dong'), ('XCD', 'East Caribbean Dollar'), ('EGP', 'Egyptian Pound'), ('SVC', 'El Salvador Colon'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('XBB', 'European Monetary Unit (E.M.U.-6)'), ('XBD', 'European Unit of Account 17(E.U.A.-17)'), ('XBC', 'European Unit of Account 9(E.U.A.-9)'), ('FKP', 'Falkland Islands Pound'), ('FJD', 'Fiji Dollar'), ('HUF', 'Forint'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('XAU', 'Gold'), ('XFO', 'Gold-Franc'), ('PYG', 'Guarani'), ('GNF', 'Guinea Franc'), ('GYD', 'Guyana Dollar'), ('HTG', 'Haitian gourde'), ('HKD', 'Hong Kong Dollar'), ('UAH', 'Hryvnia'), ('ISK', 'Iceland Krona'), ('INR', 'Indian Rupee'), ('IRR', 'Iranian Rial'), ('IQD', 'Iraqi Dinar'), ('IMP', 'Isle of Man Pound'), ('JMD', 'Jamaican Dollar'), ('JOD', 'Jordanian Dinar'), ('KES', 'Kenyan Shilling'), ('PGK', 'Kina'), ('LAK', 'Kip'), ('KWD', 'Kuwaiti Dinar'), ('AOA', 'Kwanza'), ('MMK', 'Kyat'), ('GEL', 'Lari'), ('LVL', 'Latvian Lats'), ('LBP', 'Lebanese Pound'), ('ALL', 'Lek'), ('HNL', 'Lempira'), ('SLL', 'Leone'), ('LSL', 'Lesotho loti'), ('LRD', 'Liberian Dollar'), ('LYD', 'Libyan Dinar'), ('SZL', 'Lilangeni'), ('LTL', 'Lithuanian Litas'), ('MGA', 'Malagasy Ariary'), ('MWK', 'Malawian Kwacha'), ('MYR', 'Malaysian Ringgit'), ('TMM', 'Manat'), ('MUR', 'Mauritius Rupee'), ('MZN', 'Metical'), ('MXV', 'Mexican Unidad de Inversion (UDI)'), ('MXN', 'Mexican peso'), ('MDL', 'Moldovan Leu'), ('MAD', 'Moroccan Dirham'), ('BOV', 'Mvdol'), ('NGN', 'Naira'), ('ERN', 'Nakfa'), ('NAD', 'Namibian Dollar'), ('NPR', 'Nepalese Rupee'), ('ANG', 'Netherlands Antillian Guilder'), ('ILS', 'New Israeli Sheqel'), ('RON', 'New Leu'), ('TWD', 'New Taiwan Dollar'), ('NZD', 'New Zealand Dollar'), ('KPW', 'North Korean Won'), ('NOK', 'Norwegian Krone'), ('PEN', 'Nuevo Sol'), ('MRO', 'Ouguiya'), ('TOP', 'Paanga'), ('PKR', 'Pakistan Rupee'), ('XPD', 'Palladium'), ('MOP', 'Pataca'), ('PHP', 'Philippine Peso'), ('XPT', 'Platinum'), ('GBP', 'Pound Sterling'), ('BWP', 'Pula'), ('QAR', 'Qatari Rial'), ('GTQ', 'Quetzal'), ('ZAR', 'Rand'), ('OMR', 'Rial Omani'), ('KHR', 'Riel'), ('MVR', 'Rufiyaa'), ('IDR', 'Rupiah'), ('RUB', 'Russian Ruble'), ('RWF', 'Rwanda Franc'), ('XDR', 'SDR'), ('SHP', 'Saint Helena Pound'), ('SAR', 'Saudi Riyal'), ('RSD', 'Serbian Dinar'), ('SCR', 'Seychelles Rupee'), ('XAG', 'Silver'), ('SGD', 'Singapore Dollar'), ('SBD', 'Solomon Islands Dollar'), ('KGS', 'Som'), ('SOS', 'Somali Shilling'), ('TJS', 'Somoni'), ('SSP', 'South Sudanese Pound'), ('LKR', 'Sri Lanka Rupee'), ('XSU', 'Sucre'), ('SDG', 'Sudanese Pound'), ('SRD', 'Surinam Dollar'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('SYP', 'Syrian Pound'), ('BDT', 'Taka'), ('WST', 'Tala'), ('TZS', 'Tanzanian Shilling'), ('KZT', 'Tenge'), ('XXX', 'The codes assigned for transactions where no currency is involved'), ('TTD', 'Trinidad and Tobago Dollar'), ('MNT', 'Tugrik'), ('TND', 'Tunisian Dinar'), ('TRY', 'Turkish Lira'), ('TMT', 'Turkmenistan New Manat'), ('TVD', 'Tuvalu dollar'), ('AED', 'UAE Dirham'), ('XFU', 'UIC-Franc'), ('USD', 'US Dollar'), ('USN', 'US Dollar (Next day)'), ('UGX', 'Uganda Shilling'), ('CLF', 'Unidad de Fomento'), ('COU', 'Unidad de Valor Real'), ('UYI', 'Uruguay Peso en Unidades Indexadas (URUIURUI)'), ('UYU', 'Uruguayan peso'), ('UZS', 'Uzbekistan Sum'), ('VUV', 'Vatu'), ('CHE', 'WIR Euro'), ('CHW', 'WIR Franc'), ('KRW', 'Won'), ('YER', 'Yemeni Rial'), ('JPY', 'Yen'), ('CNY', 'Yuan Renminbi'), ('ZMK', 'Zambian Kwacha'), ('ZMW', 'Zambian Kwacha'), ('ZWD', 'Zimbabwe Dollar A/06'), ('ZWN', 'Zimbabwe dollar A/08'), ('ZWL', 'Zimbabwe dollar A/09'), ('PLN', 'Zloty')], default='USD', editable=False, max_length=3),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='nCurrentPrice',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='current price (converted to USD)'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='tTimeBeg',
            field=models.DateTimeField(null=True, verbose_name='beginning date/time'),
        ),
        migrations.AddField(
            model_name='itemhit',
            name='tTimeEnd',
            field=models.DateTimeField(null=True, verbose_name='ending date/time'),
        ),
    ]
