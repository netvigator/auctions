from django.contrib import admin

from mptt.admin import MPTTModelAdmin

# Register your models here.

from .models import EbayCategory, Condition

class EbayCategoryAdmin(admin.ModelAdmin):
    list_display = ( "iMarket", "iCategoryID", "name", "iLevel",
                     "iParentID", "bLeafCategory", "iTreeVersion" )

class ConditionAdmin(admin.ModelAdmin):
    list_display = ( "iConditionID", "cTitle" )

# admin.site.register(EbayCategory, MPTTModelAdmin)
admin.site.register(EbayCategory, EbayCategoryAdmin)

admin.site.register( Condition )