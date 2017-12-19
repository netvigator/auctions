from django.contrib import admin

# Register your models here.

from .models import EbayCategory, Condition


class EbayCategoryAdmin(admin.ModelAdmin):
    list_display = ( "ebay_id", "ctitle", "ilevel", "iparent_id",
                     "bleaf_category", "iTreeVersion" )


class ConditionAdmin(admin.ModelAdmin):
    list_display = ( "ebay_id", "ctitle" )

admin.site.register(EbayCategory, EbayCategoryAdmin)

admin.site.register( Condition )