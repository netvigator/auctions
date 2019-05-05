
from core.mixins                import WereAnyReleventColsChangedBase



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


