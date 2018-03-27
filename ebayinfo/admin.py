from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from .models import EbayCategory, Condition, Market

# Register your models here.

class EbayCategoryAdmin(admin.ModelAdmin):
    list_display = ( "iEbaySiteID", "iCategoryID", "name", "iLevel",
                     "iParentID", "bLeafCategory", "iTreeVersion" )

class ConditionAdmin(admin.ModelAdmin):
    list_display = ( "iConditionID", "cTitle" )

class MarketAdmin(admin.ModelAdmin):
    list_display = (
        "cMarket", "cCountry", "cLanguage", "iEbaySiteID", "iCategoryVer",
        "cCurrencyDef", "bHasCategories" )
    readonly_fields=('iCategoryVer', )



admin.site.register( EbayCategory,  EbayCategoryAdmin)

admin.site.register( Condition,     ConditionAdmin )

admin.site.register( Market,        MarketAdmin )