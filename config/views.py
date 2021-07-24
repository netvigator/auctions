from django.views.generic   import ListView

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
        qsCollections = User.objects.exclude(
                cCollection__isnull = True ).exclude(
                cCollection = '' )
        #
        return qsCollections
