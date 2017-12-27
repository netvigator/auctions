
from django.http import HttpResponseForbidden


class DoesLoggedInUserOwnTheRowMixin(object):

    def get_object(self):
        obj = super(DoesLoggedInUserOwnTheRowMixin, self).get_object()
        if obj.iUser != self.request.user:
            return HttpResponseForbidden(
                "Permission Error -- that's not your record!")
        return obj

    
