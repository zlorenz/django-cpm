from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from core.models import Slugged, base_concrete_model, DateStamp


class Project(DateStamp, Slugged):
    user = models.ForeignKey(User, blank=True)
    description = models.TextField(blank=True)
    completion = models.IntegerField(default=0)
    start_time = models.DateField(blank=True, null=True)

    #blueprints
    #drawings

    def get_absolute_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('projects:project-update', kwargs={'pk': self.pk})

    def get_category_price(self, category):
        total = 0
        for p in self.task_set.filter(category=category):
            total += p.price
        return total

    def get_category_expense(self, category):
        total = 0
        for p in self.task_set.filter(category=category):
            total += p.expense
        return total

    def get_category_total(self, category):
        return sum(self.get_category_expense(category), self.get_category_price(category))

    def get_project_category_totals(self):
        result_dict = {}
        cat_dict = {}
        all_tasks = self.task_set.all()
        for task in all_tasks:
            try:
                cat_dict[task.category.id]
            except KeyError:
                cat_dict[task.category.id] = task.category
        for cat in cat_dict:
            cat_exp_total = self.get_category_expense(cat_dict[cat])
            cat_price_total = self.get_category_price(cat_dict[cat])
            result_dict[cat_dict[cat].id] = {
                'slug': cat_dict[cat].slug,
                'title': cat_dict[cat].title,
                'expense': cat_exp_total,
                'price': cat_price_total,
                'total': sum([cat_exp_total, cat_price_total]),
            }
        return result_dict
