from django.contrib import admin

# Register your models here.

from .models import Brand

from core.admin import admin_method_attributes

from Utils.Output import getSayYesOrNo

class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "ctitle", "_bwanted", "_ballofinterest", "_istars",
        "cnationality", "ccomment", "cexcludeif" )
    readonly_fields = ("_bwanted", "_ballofinterest", "_istars", 'ilegacykey' )
    
    @admin_method_attributes( short_description='Want anything?' )
    def _bwanted(self, obj):
        return getSayYesOrNo( obj.bwanted )
    
    @admin_method_attributes( short_description='Want everything?' )
    def _ballofinterest(self, obj):
        return getSayYesOrNo( obj.ballofinterest )
    
    @admin_method_attributes( short_description='Desireability' )
    def _istars(self, obj):
        return obj.istars



admin.site.register(Brand, BrandAdmin)