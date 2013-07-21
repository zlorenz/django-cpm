import json
from crispy_forms.utils import render_crispy_form
from django.contrib.auth.models import User

from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.forms.models import inlineformset_factory
from braces.views import JSONResponseMixin

from jsonview.decorators import json_view

from core.views import AjaxableResponseMixin

from projects.models import Project

from .models import Task, TaskCategory
from .forms import TaskForm, TaskCategoryForm



def manage_tasks(request, project_id):
    #TODO: Remove. not being used
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


class TaskListView(JSONResponseMixin, generic.ListView):
    #todo:This view needs to be redone. Using weird shit. Will keep for now for reference
    model = Task
    content_type = 'application/javascript'
    json_dumps_kwargs = {'indent': 2}
    template_name = 'tasks/task_list.html'

    def get(self, request, *arg, **kwargs):
        self.user = get_object_or_404(Project, id=self.args[0])
        project_tasks = Task.objects.filter(project=self.user)
        if request.is_ajax():
            context = {}
            for task in project_tasks:
                task_context = {
                    'title': task.title,
                    'description': task.description,
                    'project': task.project.title,
                    'status': task.get_status(),
                    'projected_completion_date': task.projected_completion_date
                }
                context[task.id] = task_context

            context.update(kwargs)
            return self.render_json_response(context)
        else:
            context = {'task_list': project_tasks}
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


class TaskListUpdateView(generic.ListView):
    model = Task
    template_name = 'tasks/task_update_json.html'


class TaskFormView(generic.CreateView):
    model = Task
    form_class = TaskForm

    @json_view
    def dispatch(self, *args, **kwargs):
        return super(TaskFormView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #TODO: Form processing needed
        form.save()
        update_url = form.instance.get_update_url()
        form_html = render_crispy_form(self.form_class())
        context = {'success': True, 'update_url': update_url, 'form_html': form_html, 'new': True}
        return context

    def form_invalid(self, form):
        form_html = render_crispy_form(form)
        return {'success': False, 'form_html': form_html}

    def get(self, request, *args, **kwargs):
        form_html = render_crispy_form(self.form_class())
        context = {'form_html': form_html}
        return context


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm

    @json_view
    def dispatch(self, *args, **kwargs):
        return super(TaskUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #TODO: Form processing needed
        form.save()
        update_url = self.object.get_update_url()
        form_html = render_crispy_form(self.form_class())
        context = {'success': True, 'update_url': update_url, 'form_html': form_html, 'new': False}
        return context

    def form_invalid(self, form):
        form.helper.form_action = self.object.get_update_url()
        form_html = render_crispy_form(form)
        return {'success': False, 'form_html': form_html}

    def get(self, request, *args, **kwargs):
        self.object = super(TaskUpdateView, self).get_object()
        form = self.form_class(instance=self.object)
        form.helper.form_action = self.object.get_update_url()
        form_html = render_crispy_form(form)
        context = {'form_html': form_html}
        return context


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:task-list')


class TaskCategoryFormView(generic.CreateView):
    model = TaskCategory
    form_class = TaskCategoryForm

    @json_view
    def dispatch(self, *args, **kwargs):
        return super(TaskCategoryFormView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #TODO: Form processing needed
        form.save()
        update_url = form.instance.get_update_url()
        form_html = render_crispy_form(self.form_class())
        context = {'success': True, 'update_url': update_url, 'form_html': form_html, 'new': True,
                   'pk': form.instance.id}
        return context

    def form_invalid(self, form):
        form_html = render_crispy_form(form)
        return {'success': False, 'form_html': form_html}

    def get(self, request, *args, **kwargs):
        form_html = render_crispy_form(self.form_class())
        context = {'form_html': form_html}
        return context


class TaskCategoryUpdateView(generic.UpdateView):
    model = TaskCategory
    form_class = TaskCategoryForm

    @json_view
    def dispatch(self, *args, **kwargs):
        return super(TaskCategoryUpdateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #TODO: Form processing needed
        form.save()
        update_url = self.object.get_update_url()
        form_html = render_crispy_form(self.form_class())
        context = {'success': True, 'update_url': update_url, 'form_html': form_html, 'new': False}
        return context

    def form_invalid(self, form):
        form.helper.form_action = self.object.get_update_url()
        form_html = render_crispy_form(form)
        return {'success': False, 'form_html': form_html}

    def get(self, request, *args, **kwargs):
        self.object = super(TaskCategoryUpdateView, self).get_object()
        form = self.form_class(instance=self.object)
        form.helper.form_action = self.object.get_update_url()
        form_html = render_crispy_form(form)
        context = {'form_html': form_html}
        return context


class TaskCategoryDeleteView(generic.DeleteView):
    model = TaskCategory
    success_url = reverse_lazy('tasks:task-list')
