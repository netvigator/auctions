from django.contrib import admin

# Register your models here.

from .models import Search, ItemFound, UserItemFound

from django.contrib.auth import get_user_model
User = get_user_model()


class SearchAdmin(admin.ModelAdmin):
    list_display = (
        'cTitle',
        'iEbayCategory',
        'cPriority',
        'cKeyWords',
        'tBegSearch',
        'tEndSearch',
        'cLastResult',)
    readonly_fields = (
        'iEbayCategory',
        'tBegSearch',
        'tEndSearch',
        'cLastResult',
        'iUser',
        'tCreate',
        'tModify')

    def save_model(self, request, obj, form, change):
        #
        if getattr( obj, "iUser", None ) is None: obj.iUser = request.user
        #
        obj.save()



class ItemFoundAdmin(admin.ModelAdmin):
    list_display = (
        'iItemNumb',
        'cTitle',
        'tCreate',
        'tTimeBeg',
        'tTimeEnd',
        'cLocation',
        'cCountry',
        'cListingType',
        'cMarket',
        'bBuyItNowable',
        'bBestOfferable',
        'lLocalCurrency',
        'lCurrentPrice',
        'dCurrentPrice',
        'iCategoryID',
        'cCategory',
        'CatHeirarchy',
        'i2ndCategoryID',
        'c2ndCategory',
        'SecondCatHeir',
        'iConditionID',
        'cCondition',
        'cSellingState',
        )
    readonly_fields = (
        'iItemNumb',
        'cTitle',
        'cLocation',
        'cCountry',
        'cMarket',
        'cGalleryURL',
        'cEbayItemURL',
        'tTimeBeg',
        'tTimeEnd',
        'bBestOfferable',
        'bBuyItNowable',
        'cListingType',
        'lLocalCurrency',
        'lCurrentPrice',
        'dCurrentPrice',
        'iCategoryID',
        'cCategory',
        'CatHeirarchy',
        'i2ndCategoryID',
        'c2ndCategory',
        'SecondCatHeir',
        'iConditionID',
        'cCondition',
        'cSellingState',
        'tCreate' )

    def CatHeirarchy( self, obj ):
        #
        return obj.iCatHeirarchy.cCatHierarchy

    def SecondCatHeir( self, obj ):
        #
        if obj.i2ndCatHeirarchy is None:
            return None
        else:
            return obj.i2ndCatHeirarchy.cCatHierarchy


class UserItemFoundAdmin(admin.ModelAdmin):

    list_display = (
        'iItemNumb',
        'iHitStars',
        'bGetPictures',
        'tLook4Hits',
        'iSearch',
        'iModel',
        'iBrand',
        'iCategory',
        'cWhereCategory',
        'bListExclude',
        'tGotPics',
        'bAuction',
        'iUser',
        'tCreate',
        'tModify',
        'tRetrieved',
        'tRetrieveFinal' )

    readonly_fields = (
        'iItemNumb',
        'iHitStars',
        'bGetPictures',
        'tLook4Hits',
        'iSearch',
        'iModel',
        'iBrand',
        'iCategory',
        'cWhereCategory',
        'bListExclude',
        'tGotPics',
        'bAuction',
        'iUser',
        'tCreate',
        'tModify',
        'tRetrieved',
        'tRetrieveFinal' )

admin.site.register(Search,SearchAdmin)
admin.site.register(ItemFound,ItemFoundAdmin)
admin.site.register(UserItemFound, UserItemFoundAdmin)
