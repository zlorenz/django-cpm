from django.db import models
from django.core.urlresolvers import reverse
from django.utils.timesince import timesince, timeuntil
from django.utils.translation import ugettext_lazy as _

from core.models import Slugged, base_concrete_model, DateStamp

from cpm.projects.models import Project
from changes.models import ChangeOrder


class Task(Slugged):
    project = models.ForeignKey(Project)
    status = models.BooleanField(choices=[(0, 'In Progress'), (1, 'Complete')])
    projected_completion_date = models.DateField(_("Projected Completion Date"),
                                                 blank=True, null=True)
    completion_date = models.DateField(_("Actual Completion Date"),
                                       blank=True, null=True)
    description = models.TextField(blank=True)
    expense = models.IntegerField(blank=True)
    price = models.IntegerField(blank=True)
    category = models.ForeignKey('TaskCategory')
    change_order = models.ForeignKey(ChangeOrder, blank=True)

    def get_absolute_url(self):
        return reverse('tasks:task-detail', kwargs={'pk': self.pk})

    def due_date_until(self):
        return timeuntil(self.projected_completion_date)

    def due_date_since(self):
        return timesince(self.projected_completion_date)

    due_date_since.short_description = _("Late by")
    due_date_until.short_description = _("Due in")

class TaskCategory(Slugged):

    def get_project_category_total(self, project):
        total = 0
        for p in project.task_set.all():
            total += p.price
        return total