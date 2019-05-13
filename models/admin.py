from django.contrib     import admin

from core.admin         import admin_method_attributes

from .models            import Model

from pyPks.Utils.Output import getSayYesOrNo
from pyPks.String.Get   import getUpToLenSplitOnWhite


class ModelAdmin(admin.ModelAdmin):
    list_display = (
        "cTitle",
        "_cKeyWords", "_iStars", "_iBrand", "_iCategory",
        "_cComment" )
    readonly_fields = (
        "_cKeyWords", "_iStars", "_iBrand", "_iCategory",
        "_cComment", 'iLegacyKey' )

    @admin_method_attributes( short_description='Key words', allow_tags=True )
    def _cKeyWords(self, obj):
        return str( obj.cKeyWords ).replace( ' ', '&nbsp;' )

    #@admin_method_attributes( short_description='Required?' )
    #def _bKeyWordRequired(self, obj):
        #return getSayYesOrNo( obj.bKeyWordRequired )

    @admin_method_attributes( short_description='Desireability' )
    def _iStars(self, obj):
        return obj.iStars

    @admin_method_attributes( short_description='Brand', allow_tags=True )
    def _iBrand(self, obj):
        return str( obj.iBrand ).replace( ' ', '&nbsp;' )

    @admin_method_attributes( short_description='Category', allow_tags=True )
    def _iCategory(self, obj):
        return str( obj.iCategory ).replace( ' ', '&nbsp;' )

    def _cComment(self, obj):

        sComment = str( obj.cComment )

        if len( sComment ) > 80:
            sComment = getUpToLenSplitOnWhite( sComment, 76 ) + ' ...'

        return sComment


admin.site.register(Model, ModelAdmin)
