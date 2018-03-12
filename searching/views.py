from core.views             import ( CreateViewGotCrispy, DeleteViewGotModel,
                                     DetailViewGotModel,  ListViewGotModel,
                                     UpdateViewGotCrispy )

from .forms                 import ItemFoundForm
from .mixins                import SearchViewSuccessPostFormValidMixin
from .models                import Search, ItemFound, UserItemFound

# Create your views here.

tModelFields = (
    'cTitle',
    'cKeyWords',
    'iDummyCategory',
    'cPriority', )


class SearchCreateView( SearchViewSuccessPostFormValidMixin, CreateViewGotCrispy ):

    template_name   = 'searching/add.html'
    success_message = 'New Search record successfully saved!!!!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        form.which = 'Create'
        return form



class SearchIndexView( ListViewGotModel ):  
    
    template_name   = 'searching/index.html'
    model           = Search


class SearchDetailView( DetailViewGotModel ):
    
    model           = Search
    template_name   = 'searching/detail.html'



class SearchDeleteView( DeleteViewGotModel ):

    template_name   = 'confirm_delete.html'
    success_message = 'Search record successfully deleted!!!!'




class SearchUpdateView( SearchViewSuccessPostFormValidMixin, UpdateViewGotCrispy ):

    template_name   = 'searching/edit.html'
    success_message = 'Search record update successfully saved!!!!'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request= self.request
        form.which  = 'Update'
        return form




class ItemsFoundIndexView( ListViewGotModel ):  
    
    template_name       = 'searching/items_found_index.html'
    model               = ItemFound
    context_object_name = 'items_found_list'


    def get_queryset(self):
        return self.model.objects.filter(
                pk__in = UserItemFound.objects
                    .filter( iUser = self.request.user )
                    .values_list( 'iItemFound', flat=True ) )



class ItemFoundDetailView( DetailViewGotModel ):
    
    model           = ItemFound
    template_name   = 'searching/items_found_detail.html'
    form_class      = ItemFoundForm

