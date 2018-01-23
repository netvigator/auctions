



class EbayCategoryFormValidMixin(object):

    def form_valid(self, form):
        #
        if 'Cancel' in self.request.POST:
            return HttpResponseRedirect(self.get_success_url())
        #
        form.instance.iUser = self.request.user
        #
        form.instance.iEbayCategory = form.cleaned_data.get('iEbayCategory')
        #
        return super().form_valid(form)
