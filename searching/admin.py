from django.contrib import admin

# Register your models here.

from .models import Search, ItemFound, UserItemFound

from django.contrib.auth import get_user_model
User = get_user_model()


class SearchAdmin(admin.ModelAdmin):
    list_display = (
        'cTitle','iEbayCategory','cPriority','cKeyWords',
        'tSearchStarted','tSearchComplete',
        'cLastResult',)
    readonly_fields = (
        'iEbayCategory','tSearchStarted','tSearchComplete',
        'cLastResult','iUser','tCreate',
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
        'cLocation', 
        'cCountry', 
        'cMarket', 
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
        'i2ndCategoryID', 
        'c2ndCategory', 
        'iConditionID', 
        'cCondition', 
        'cSellingState', 
        'tCreate' )
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
        'i2ndCategoryID', 
        'c2ndCategory', 
        'cCatHeirarchy', 
        'iConditionID', 
        'cCondition', 
        'cSellingState', 
        'tCreate' )

admin.site.register(Search,SearchAdmin)
admin.site.register(ItemFound,ItemFoundAdmin)
