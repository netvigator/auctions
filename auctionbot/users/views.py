from django.urls                import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

from core.mixins                import DoPostCanCancelMixin
from .models import User

tUserFields = (
    'name',
    'iEbaySiteID',
    'cCollection',
    'cBio',
    'cLocation',
    'email',
    'zTimeZone'
    )

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/user_detail.html'


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})


class UserUpdateView( DoPostCanCancelMixin, LoginRequiredMixin, UpdateView ):

    fields = tUserFields[:-1]

    # we already imported User in the view code above, remember?
    model = User
    template_name = 'users/user_form.html'

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('users:detail',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User

    fields = tUserFields

    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/user_list.html'
