from django             import forms

from django.forms       import ModelForm

from keepers            import dItemFields # in __init__.py

from .models            import Keeper

# ### forms validate the incoming data against the database      ###
# ### additional custom validation logic can be implemented here ###
# ### crispy forms adds automatic layout functionality           ###

tItemFields = tuple( dItemFields.keys() )

class KeeperForm(ModelForm):
    #
    '''using a form to validate incoming info from ebay'''
    #
    class Meta:
        model   = Keeper
        fields  = tItemFields




