from django.contrib import admin

# Register your models here.

from .models import Search

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


admin.site.register(Search,SearchAdmin)
