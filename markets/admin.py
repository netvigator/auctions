from django.contrib import admin

# Register your models here.

from .models import Market

class MarketAdmin(admin.ModelAdmin):
    list_display = ( "cmarket", "ccountry", "clanguage", "iebaysiteid" ) 


admin.site.register(Market,MarketAdmin)