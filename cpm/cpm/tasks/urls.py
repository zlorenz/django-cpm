try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

from .views import TaskFormView, TaskUpdateView, TaskDeleteView, TaskAJAXView, TaskListView, TaskDetailView, manage_tasks

urlpatterns = patterns('cpm.tasks',
                       url(r'^create/$', TaskFormView.as_view(), name='task-form'),
                       url(r'^manage/(?P<project_id>\d+)/$', manage_tasks, name='task-manager'),
                       url(r'^update/(?P<pk>\d+)/$', TaskUpdateView.as_view(), name='task-update'),
                       url(r'^delete/(?P<pk>\d+)/$', TaskDeleteView.as_view(), name='task-delete'),
                       url(r'^(?P<pk>\d+)/$', TaskDetailView.as_view(), name='task-detail'),
                       url(r'^$', TaskListView.as_view(), name='task-list'),
                       )

