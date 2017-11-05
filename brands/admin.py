from django.contrib import admin

# Register your models here.

from .models import Brand

from core.utils import admin_method_attributes

class BrandAdmin(admin.ModelAdmin):
    list_display = ("ctitle", "_bwanted", "_ballofinterest", "_istars")
    read_only_fields = ("_bwanted", "_ballofinterest", "_istars")
    
    @admin_method_attributes(short_description='Want anything?', allow_tags=True)
    def _bwanted(self, obj):
        return obj.bwanted
    
    @admin_method_attributes(short_description='Want everything?', allow_tags=True)
    def _ballofinterest(self, obj):
        return obj.ballofinterest
    
    @admin_method_attributes(short_description='Desireability', allow_tags=True)
    def _istars(self, obj):
        return obj.istars
    


admin.site.register(Brand, BrandAdmin)