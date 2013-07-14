import json

from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.forms.models import inlineformset_factory
from braces.views import JSONResponseMixin

from projects.models import Project

from .models import Task
from .forms import TaskForm


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response


class TaskAJAXView(JSONResponseMixin, generic.DetailView):
    model = Task
    content_type = 'application/javascript'
    json_dumps_kwargs = {'indent': 2}

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        context_dict = {
            'title': self.object.title,
            'description': self.object.description,
            'project': self.object.project.title,
            'status': self.object.status,
            'projected_completion_date': self.object.projected_completion_date
        }

        return self.render_json_response(context_dict)


class TaskListView(JSONResponseMixin, generic.ListView):
    model = Task
    content_type = 'application/javascript'
    json_dumps_kwargs = {'indent': 2}
    template_name = 'tasks/task_list.html'

    def get(self, request, *arg, **kwargs):
        if request.is_ajax():
            context = {}

            for task in Task.objects.all():
                task_context = {
                    'title': task.title,
                    'description': task.description,
                    'project': task.project.title,
                    'status': task.status,
                    'projected_completion_date': task.projected_completion_date
                }
                context[task.id] = task_context

            context.update(kwargs)
            return self.render_json_response(context)
        else:
            context = {'task_list': Task.objects.all()}
            return render(request, self.template_name, context)


class TaskDetailView(JSONResponseMixin, generic.DetailView):
    model = Task
    content_type = 'application/javascript'
    json_dumps_kwargs = {'indent': 2}
    template_name = 'tasks/task_detail.html'

    def get(self, request, *arg, **kwargs):
        if request.is_ajax():
            context = {}
            context.update(kwargs)

            context += {
                'title': self.object.title,
                'description': self.object.description,
                'project': self.object.project.title,
                'status': self.object.status,
                'projected_completion_date': self.object.projected_completion_date
            }

            return self.render_json_response(context)
        else:
            context = {'task': self.get_object(self.get_queryset())}
            return render(request, self.template_name, context)


class TaskFormView(AjaxableResponseMixin, generic.CreateView):
    model = Task
    form_class = TaskForm


def manage_tasks(request, project_id):
    project = Project.objects.get(pk=project_id)
    TaskFormSet = inlineformset_factory(Project, Task, form=TaskForm)
    if request.method == 'POST':
        formset = TaskFormSet(request.POST, request.FILES, instance=project)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(project.get_absolute_url())
    else:
        formset = TaskFormSet(instance=project)
    return render_to_response('tasks/manage_tasks.html', {'formset': formset, 'project': project})


class TaskUpdateView(AjaxableResponseMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task-list')

