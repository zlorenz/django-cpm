try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import UserListView

urlpatterns = patterns('accounts.views',
                       url(r'^signup/$', 'signup', name='signup'),
                       url(r'^profile/(?P<id>.*)/$', 'profile', name='profile'),
                       url("^profile/", "profile_redirect", name="profile_redirect"),
                       url(r'^$', UserListView.as_view(), name='user-list'),
)
