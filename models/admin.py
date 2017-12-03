from django.contrib import admin

# Register your models here.

from core.admin import admin_method_attributes

from .models import Model

from Utils.Output   import getSayYesOrNo
from String.Get     import getUpToLenSplitOnWhite

class ModelAdmin(admin.ModelAdmin):
    list_display = (
        "ctitle", 
        "_ckeywords","_bkeywordrequired", "_istars", "_ibrand", "_icategory",
        "_ccomment" )
    readonly_fields = (
        "_ckeywords", "_bkeywordrequired", "_istars", "_ibrand", "_icategory",
        "_ccomment", 'ilegacykey' )

    @admin_method_attributes( short_description='Key words', allow_tags=True )
    def _ckeywords(self, obj):
        return str( obj.ckeywords ).replace( ' ', '&nbsp;' )

    @admin_method_attributes( short_description='Required?' )
    def _bkeywordrequired(self, obj):
        return getSayYesOrNo( obj.bkeywordrequired )

    @admin_method_attributes( short_description='Desireability' )
    def _istars(self, obj):
        return obj.istars

    @admin_method_attributes( short_description='Brand', allow_tags=True )
    def _ibrand(self, obj):
        return str( obj.ibrand ).replace( ' ', '&nbsp;' )

    @admin_method_attributes( short_description='Category', allow_tags=True )
    def _icategory(self, obj):
        return str( obj.icategory ).replace( ' ', '&nbsp;' )

    def _ccomment(self, obj):
        
        sComment = str( obj.ccomment )
        
        if len( sComment ) > 80:
            sComment = getUpToLenSplitOnWhite( sComment, 76 ) + ' ...'
                    
        return sComment


admin.site.register(Model, ModelAdmin)