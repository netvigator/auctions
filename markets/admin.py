from django.contrib import admin

# Register your models here.

from .models import Market

class MarketAdmin(admin.ModelAdmin):
    list_display = (
        "cMarket", "cCountry", "cLanguage", "iEbaySiteID", "iCategoryVer",
        "cCurrencyDef", "bHasCategories" )
    readonly_fields=('iCategoryVer', )



admin.site.register(Market,MarketAdmin)