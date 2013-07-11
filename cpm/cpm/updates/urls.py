try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import UpdateUserFormView, UpdateFormView, UpdateUpdateView, UpdateDeleteView, UpdateDetailView, UpdateListView

urlpatterns = patterns('cpm.updates',
                       url(r'^create/([\d-]+)/$', UpdateUserFormView.as_view(), name='update-user-form'),
                       url(r'^create/$', UpdateFormView.as_view(), name='update-form'),
                       url(r'^update/(?P<pk>\d+)/$', UpdateUpdateView.as_view(), name='update-update'),
                       url(r'^delete/(?P<pk>\d+)/$', UpdateDeleteView.as_view(), name='update-delete'),
                       url(r'^(?P<pk>\d+)/$', UpdateDetailView.as_view(), name='update-detail'),
                       url(r'^$', UpdateListView.as_view(), name='update-list'),
)
