import json

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.views.generic.base import RedirectView

from core.views import AjaxableResponseMixin

from .forms import ProjectForm
from tasks.forms import TaskForm
from .models import Project




class ProjectDetailView(AjaxableResponseMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = {
            'form': TaskForm(),
        }
        context.update(kwargs)
        return super(ProjectDetailView, self).get_context_data(**context)


class ProjectListView(generic.ListView):
    model = Project

    def get_queryset(self):
        self.user = get_object_or_404(User, id=self.args[0])
        return Project.objects.filter(user=self.user)


class ProjectFormView(AjaxableResponseMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm


class ProjectRedirectView(RedirectView):
    """
    redirects users to their project view
    """
    permanent = False
    query_string = True

    def get_redirect_url(self, **kwargs):
        user = self.request.user.id
        return reverse('projects:project-list', args=(user,))


'''
def project_redirect(request):
    return redirect(ProjectListView.as_view(), args=(request.user.id,))
def manage_tasks(request, project_id):
    project = Project.objects.get(pk=project_id)
    ProjectFormSet = inlineformset_factory(Project, Project, form=ProjectForm)
    if request.method == 'POST':
        formset = ProjectFormSet(request.POST, request.FILES, instance=project)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(project.get_absolute_url())
    else:
        formset = ProjectFormSet(instance=project)
    return render_to_response('projects/manage_projects.html', {'formset': formset, 'project': project})
'''


class ProjectUpdateView(AjaxableResponseMixin, generic.UpdateView):
    model = Project


class ProjectDeleteView(generic.DeleteView):
    model = Project
    success_url = reverse_lazy('projects:project-list')
