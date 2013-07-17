try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import ChangeOrderUserFormView, ChangeOrderFormView, ChangeOrderChangeOrderView, ChangeOrderDeleteView, ChangeOrderDetailView, ChangeOrderListView

urlpatterns = patterns('changes',
                       url(r'^create/([\d-]+)/$', ChangeOrderUserFormView.as_view(), name='change-user-form'),
                       url(r'^create/$', ChangeOrderFormView.as_view(), name='change-form'),
                       url(r'^change/(?P<pk>\d+)/$', ChangeOrderChangeOrderView.as_view(), name='change-change'),
                       url(r'^delete/(?P<pk>\d+)/$', ChangeOrderDeleteView.as_view(), name='change-delete'),
                       url(r'^(?P<pk>\d+)/$', ChangeOrderDetailView.as_view(), name='change-detail'),
                       url(r'^$', ChangeOrderListView.as_view(), name='change-list'),
                       )
