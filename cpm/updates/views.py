from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.urlresolvers import reverse_lazy

from projects.models import Project

from .models import Update
from .forms import UpdateUserForm


class UpdateListView(generic.ListView):
    model = Update


class UpdateDetailView(generic.DetailView):
    model = Update


class UpdateFormView(generic.CreateView):
    model = Update
    template_name = 'updates/update_form.html'


class UpdateUserFormView(generic.CreateView):
    model = Update
    form_class = UpdateUserForm

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, id=self.args[0])
        return super(UpdateUserFormView, self).form_valid(form)


class UpdateUpdateView(generic.UpdateView):
    model = Update


class UpdateDeleteView(generic.DeleteView):
    model = Update
    success_url = reverse_lazy('updates:update-list')

