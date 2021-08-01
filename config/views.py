from django.views.generic   import ListView, DetailView

from auctionbot.users.models import User

tUserFields = (
    'iEbaySiteID',
    'cCollection'
    )

class CollectionsListView(ListView):

    # context_object_name = 'user_list' # default
    template_name = 'pages/home.html'
    model  = User
    fields = tUserFields

    def get_queryset(self):
        #
        if not self.request.session or not self.request.session.session_key:
            self.request.session.save()
        #
        qsCollections = User.objects.exclude(
                cCollection__isnull = True ).exclude(
                cCollection = '' )
        #
        return qsCollections


class UserVisitView( DetailView):
    model = User
    template_name = 'users/visiting.html'

    def get_context_data( self, **kwargs ):
        #
        context = super().get_context_data(**kwargs)
        #
        self.request.session[   'visiting'] = context[ 'object' ].id
        self.request.session['is_visiting'] = True
        #
        print( 'set request.session.visiting to', context[ 'object' ],
                'id:', context[ 'object' ].id )
        #
        return context
