from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.urlresolvers import reverse_lazy

from projects.models import Project

from .models import ChangeOrder


class ChangeOrderListView(generic.ListView):
    model = ChangeOrder


class ChangeOrderDetailView(generic.DetailView):
    model = ChangeOrder


class ChangeOrderFormView(generic.CreateView):
    model = ChangeOrder


class ChangeOrderUserFormView(generic.CreateView):
    model = ChangeOrder

    def form_valid(self, form):
        form.instance.project = get_object_or_404(Project, id=self.args[0])
        return super(ChangeOrderUserFormView, self).form_valid(form)


class ChangeOrderChangeOrderView(generic.UpdateView):
    model = ChangeOrder


class ChangeOrderDeleteView(generic.DeleteView):
    model = ChangeOrder
    success_url = reverse_lazy('changes:change-list')
