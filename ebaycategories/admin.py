from django.contrib import admin

# Register your models here.

from .models import EbayCategory, Condition


class EbayCategoryAdmin(admin.ModelAdmin):
    list_display = ( "ebay_id", "cTitle", "iLevel", "iParent_ID",
                     "bLeafCategory", "iTreeVersion" )


class ConditionAdmin(admin.ModelAdmin):
    list_display = ( "ebay_id", "cTitle" )

admin.site.register(EbayCategory, EbayCategoryAdmin)

admin.site.register( Condition )