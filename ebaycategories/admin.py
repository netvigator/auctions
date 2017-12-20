from django.contrib import admin

# Register your models here.

from .models import EbayCategory, Condition


class EbayCategoryAdmin(admin.ModelAdmin):
    list_display = ( "iMarket", "iCategoryID", "cTitle", "iLevel",
                     "iParent_ID", "bLeafCategory", "iTreeVersion" )

class ConditionAdmin(admin.ModelAdmin):
    list_display = ( "iConditionID", "cTitle" )

admin.site.register(EbayCategory, EbayCategoryAdmin)

admin.site.register( Condition )