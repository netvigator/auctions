from django.core.urlresolvers   import reverse
from django.http                import HttpResponseRedirect
from django.urls                import reverse_lazy

from .forms                     import SearchAddOrUpdateForm
from .models                    import Search




class SearchViewSuccessPostFormValidMixin(object):

    model           = Search
    success_url     = reverse_lazy('searching:index')
    form_class      = SearchAddOrUpdateForm

    def form_valid(self, form):
        #
        if 'cancel' in self.request.POST:
            return HttpResponseRedirect(self.get_success_url())
        #
        form.instance.iUser = self.request.user
        #
        form.instance.iEbayCategory = form.cleaned_data.get('iEbayCategory')
        #
        return super( SearchViewSuccessPostFormValidMixin, self ).form_valid(form)

