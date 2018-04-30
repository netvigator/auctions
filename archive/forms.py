from django             import forms

from django.forms       import ModelForm

from archive            import dItemFields # in __init__.py

from .models            import Item


tItemFields = tuple( dItemFields.keys() )

class ItemForm(ModelForm):
    #
    '''using a form to validate incoming info from ebay'''
    #
    class Meta:
        model   = Item
        fields  = tItemFields



 
