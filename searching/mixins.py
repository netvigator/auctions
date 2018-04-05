from django.core.urlresolvers   import reverse
from django.http                import HttpResponseRedirect
from django.urls                import reverse_lazy

from core.mixins                import WereAnyReleventColsChangedBase

from .models                    import Search, UserItemFound




class SearchViewSuccessPostFormValidMixin(object):

    model           = Search
    success_url     = reverse_lazy('searching:index')

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




class AnyReleventHitStarColsChangedMixin( WereAnyReleventColsChangedBase ):
    '''
    for testing whether any HitStar relevant fields have changed 
    '''

    def redoHitStars( self, form ):
        #
        iHitStars = 0
        #
        if (    form.instance.iModel and
                form.instance.iBrand and
                form.instance.iCategory ):
            #
            iHitStars = (
                    form.instance.iModel.iStars *
                    form.instance.iBrand.iStars *
                    form.instance.iCategory.iStars )
            #
        #
        form.instance.iHitStars = iHitStars

    def form_valid( self, form ):
        #
        if self.anyReleventColsChanged( form, self.tHitStarRelevantCols ):
            #
            self.redoHitStars( form )
            #
        #
        return super(
                AnyReleventHitStarColsChangedMixin, self ).form_valid( form )

