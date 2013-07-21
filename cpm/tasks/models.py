from django.db import models
from django.core.urlresolvers import reverse
from django.utils.timesince import timesince, timeuntil
from django.utils.translation import ugettext_lazy as _

from core.models import Slugged, base_concrete_model, DateStamp

from projects.models import Project
from changes.models import ChangeOrder


class Task(Slugged):
    project = models.ForeignKey(Project)
    projected_completion_date = models.DateField(_("Projected Completion Date"),
                                                 blank=True, null=True)
    completion_date = models.DateField(_("Actual Completion Date"),
                                       blank=True, null=True)
    description = models.TextField(blank=True)
    expense = models.IntegerField(blank=True)
    price = models.IntegerField(blank=True)
    category = models.ForeignKey('TaskCategory')
    change_order = models.ManyToManyField(ChangeOrder, blank=True)

    def get_absolute_url(self):
        return reverse('tasks:task-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('tasks:task-update', kwargs={'pk': self.pk})

    def due_date_until(self):
        return timeuntil(self.projected_completion_date)

    def due_date_since(self):
        return timesince(self.projected_completion_date)

    def get_status(self):
        if self.project.start_time:
            if self.completion_date:
                result = 'Completed %s' % str(self.completion_date)
            else:
                result = 'In progress'
        else:
            result = '%s not started' % self.project.title
        return result

    def get_project_category_totals(self):
        result_dict = {}
        all_categories = TaskCategory.objects.all()
        all_tasks = Task.objects.filter(project=self.project)
        for cat in all_categories:
            cat_tasks = all_tasks.filter(category=cat)
            cat_exp_total = sum(cat_tasks.values_list('expense', flat=True))
            cat_price_total = sum(cat_tasks.values_list('price', flat=True))
            result_dict[cat.slug] = {
                'id': cat.id,
                'title': cat.title,
                'expense': cat_exp_total,
                'price': cat_price_total,
                'total': sum([cat_exp_total, cat_price_total]),
                'tasks': cat_tasks
            }
        return result_dict

    due_date_since.short_description = _("Late by")
    due_date_until.short_description = _("Due in")

class TaskCategory(Slugged):
    #todo: add category description

    def get_project_category_total(self, project):
        total = 0
        for p in project.task_set.all():
            total += p.price
        return total

    def get_absolute_url(self):
        return reverse('tasks:task-category-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('tasks:task-category-update', kwargs={'pk': self.pk})
