from django.contrib import admin

# Register your models here.

from .models import Market

class MarketAdmin(admin.ModelAdmin):
    list_display = ( "cmarket", "ccountry", "clanguages" ) 


admin.site.register(Market,MarketAdmin)