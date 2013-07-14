try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import *

urlpatterns = patterns('projects',
                       url(r'^create/$', ProjectFormView.as_view(), name='project-form'),
                       #url(r'^manage/(?P<project_id>\d+)/$', manage_projects, name='project-manager'),
                       url(r'^update/(?P<pk>\d+)/$', ProjectUpdateView.as_view(), name='project-update'),
                       url(r'^delete/(?P<pk>\d+)/$', ProjectDeleteView.as_view(), name='project-delete'),
                       #url(r'^users/([\d-]+)/$', ProjectUserListView.as_view(), name='project-user-list'),
                       url(r'^projects/(?P<pk>\d+)/$', ProjectDetailView.as_view(), name='project-detail'),
                       url(r'^([\d-]+)/$', ProjectListView.as_view(), name='project-list'),
                       url(r'^$', ProjectRedirectView.as_view(), name='project-redirect'),
)
