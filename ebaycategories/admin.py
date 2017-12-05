from django.contrib import admin

# Register your models here.

from .models import EbayCategory


class EbayCategoryAdmin(admin.ModelAdmin):
    list_display = ( "ebay_id", "ctitle", "ilevel", "iparent_id", "bleaf_category", "iTreeVersion" ) 


admin.site.register(EbayCategory, EbayCategoryAdmin)