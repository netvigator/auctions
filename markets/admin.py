from django.contrib import admin

# Register your models here.

from .models import Market

class MarketAdmin(admin.ModelAdmin):
    list_display = (
        "cmarket", "ccountry", "clanguage", "iebaysiteid", "icategoryver",
        "ccurrencydef", "bhascategories" )
    readonly_fields=('icategoryver', )



admin.site.register(Market,MarketAdmin)