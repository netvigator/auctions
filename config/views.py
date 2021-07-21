from django.urls            import reverse
from django.views.generic   import ListView

from auctionbot.users.models import User

tUserFields = (
    'name',
    'iEbaySiteID',
    'cCollection'
    )

class CollectionsListView(ListView):

    # context_object_name = 'user_list' # default
    template_name = 'pages/home.html'
    model  = User
    fields = tUserFields
