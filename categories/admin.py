from django.contrib import admin

# Register your models here.

from .models import Category

from core.admin import admin_method_attributes

from Utils.Output import getSayYesOrNo

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "ctitle", 
        "_ckeywords","_bkeywordrequired", "_ballofinterest", "_istars",
        "_bwantpair", "_baccessory", "_bcomponent", "_ifamily" )
    read_only_fields = (
        "_ckeywords", "_bkeywordrequired", "_ballofinterest",
        "_istars", "_bwantpair", "_baccessory", "_bcomponent", "_ifamily" )

    @admin_method_attributes( short_description='Key words' )
    def _ckeywords(self, obj):
        return obj.ckeywords

    @admin_method_attributes( short_description='Required?' )
    def _bkeywordrequired(self, obj):
        return getSayYesOrNo( obj.bkeywordrequired )

    @admin_method_attributes( short_description='Get all?' )
    def _ballofinterest(self, obj):
        return getSayYesOrNo( obj.ballofinterest )

    @admin_method_attributes( short_description='Desireability' )
    def _istars(self, obj):
        return obj.istars

    @admin_method_attributes( short_description='Want Pair?' )
    def _bwantpair(self, obj):
        return getSayYesOrNo( obj.bwantpair )


    @admin_method_attributes( short_description='Accessory?' )
    def _baccessory(self, obj):
        return getSayYesOrNo( obj.baccessory )

    @admin_method_attributes( short_description='Component?' )
    def _bcomponent(self, obj):
        return getSayYesOrNo( obj.bcomponent )

    @admin_method_attributes( short_description='Family' )
    def _ifamily(self, obj):
        return obj.ifamily



admin.site.register(Category,CategoryAdmin)