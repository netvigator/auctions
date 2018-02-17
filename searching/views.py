from core.views             import (
                                CreateViewGotCrispy, DeleteViewGotModel,
                                DetailViewGotModel,  ListViewGotModel,
                                UpdateViewGotCrispy )

from .mixins                import SearchFormValidSuccessPostMixin
from .models                import Search

# Create your views here.

tModelFields = (
    'cTitle',
    'cKeyWords',
    'iDummyCategory',
    'cPriority', )


class SearchCreate( SearchFormValidSuccessPostMixin, CreateViewGotCrispy ):

    template_name   = 'searching/add.html'
    success_message = 'New Search record successfully saved!!!!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        form.which = 'Create'
        return form



class IndexView( ListViewGotModel ):  
    
    template_name   = 'searching/index.html'
    model           = Search


class SearchDetail( DetailViewGotModel ):
    
    model           = Search
    template_name   = 'searching/detail.html'



class SearchDelete( DeleteViewGotModel ):

    template_name   = 'confirm_delete.html'
    success_message = 'Search record successfully deleted!!!!'




class SearchUpdate(  SearchFormValidSuccessPostMixin, UpdateViewGotCrispy ):

    template_name   = 'searching/edit.html'
    success_message = 'Search record update successfully saved!!!!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        form.which = 'Update'
        return form



