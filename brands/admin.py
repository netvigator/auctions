from django.contrib     import admin

from .models            import Brand

from core.admin         import admin_method_attributes

from pyPks.Utils.Output import getSayYesOrNo

class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "cTitle", "_bWanted", "_bAllOfInterest", "_iStars",
        "cNationality", "cComment", "cExcludeIf" )
    readonly_fields = ("_bWanted", "_bAllOfInterest", "_iStars", 'iLegacyKey' )

    @admin_method_attributes( short_description='Want anything?' )
    def _bWanted(self, obj):
        return getSayYesOrNo( obj.bWanted)

    @admin_method_attributes( short_description='Want everything?' )
    def _bAllOfInterest(self, obj):
        return getSayYesOrNo( obj.bAllOfInterest )

    @admin_method_attributes( short_description='Desireability' )
    def _iStars(self, obj):
        return obj.iStars



admin.site.register(Brand, BrandAdmin)
