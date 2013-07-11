try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import MessageFormView, MessageUpdateView, MessageDeleteView, MessageListView, MessageDetailView

urlpatterns = patterns('cpm.tasks',
                       url(r'^create/$', MessageFormView.as_view(), name='message-form'),
                       url(r'^update/(?P<pk>\d+)/$', MessageUpdateView.as_view(), name='message-update'),
                       url(r'^delete/(?P<pk>\d+)/$', MessageDeleteView.as_view(), name='message-delete'),
                       url(r'^message/(?P<pk>\d+)/$', MessageDetailView.as_view(), name='message-detail'),
                       url(r'^([\d-]+)$', MessageListView.as_view(), name='message-list'),
                       )
