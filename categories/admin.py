from django.contrib import admin

# Register your models here.

from .models import Category

from core.admin import admin_method_attributes

from Utils.Output import getSayYesOrNo

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "cTitle", 
        "_cKeyWords", "_bAllOfInterest", "_iStars",
        "_bWantPair", "_bAccessory", "_bComponent", "_iFamily" )
    readonly_fields = (
        "_cKeyWords", "_bAllOfInterest",
        "_iStars", "_bWantPair", "_bAccessory", "_bComponent", "_iFamily",
        'iLegacyKey' )

    @admin_method_attributes( short_description='Key words' )
    def _cKeyWords(self, obj):
        return obj.cKeyWords

    #@admin_method_attributes( short_description='Required?' )
    #def _bKeyWordRequired(self, obj):
        #return getSayYesOrNo( obj.bKeyWordRequired )

    @admin_method_attributes( short_description='Get all?' )
    def _bAllOfInterest(self, obj):
        return getSayYesOrNo( obj.bAllOfInterest )

    @admin_method_attributes( short_description='Desireability' )
    def _iStars(self, obj):
        return obj.iStars

    @admin_method_attributes( short_description='Want Pair?' )
    def _bWantPair(self, obj):
        return getSayYesOrNo( obj.bWantPair )


    @admin_method_attributes( short_description='Accessory?' )
    def _bAccessory(self, obj):
        return getSayYesOrNo( obj.bAccessory )

    @admin_method_attributes( short_description='Component?' )
    def _bComponent(self, obj):
        return getSayYesOrNo( obj.bComponent )

    @admin_method_attributes( short_description='Family' )
    def _iFamily(self, obj):
        return obj.iFamily



admin.site.register(Category,CategoryAdmin)