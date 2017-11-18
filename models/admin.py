from django.contrib import admin

# Register your models here.

from core.admin import admin_method_attributes

from.models import Model

from Utils.Output import getSayYesOrNo

class ModelAdmin(admin.ModelAdmin):
    list_display = (
        "ctitle", 
        "_ckeywords","_bkeywordrequired", "_istars", "_ibrand", "_icategory" )
    read_only_fields = (
        "_ckeywords", "_bkeywordrequired", "_istars", "_ibrand", "_icategory" )

    @admin_method_attributes( short_description='Key words' )
    def _ckeywords(self, obj):
        return obj.ckeywords

    @admin_method_attributes( short_description='Required?' )
    def _bkeywordrequired(self, obj):
        return getSayYesOrNo( obj.bkeywordrequired )

    @admin_method_attributes( short_description='Desireability' )
    def _istars(self, obj):
        return obj.istars

    @admin_method_attributes( short_description='Brand' )
    def _ibrand(self, obj):
        return obj.ibrand

    @admin_method_attributes( short_description='Category' )
    def _icategory(self, obj):
        return obj.icategory



admin.site.register(Model, ModelAdmin)