from django.db import models
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from core.models import Slugged, base_concrete_model, DateStamp

from projects.models import Project
from tasks.models import Task


class Update(Slugged):
    project = models.ForeignKey(Project)
    description = models.TextField(blank=True)
    publish_date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('updates:update-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('updates:update-update', kwargs={'pk': self.pk})

    def add_tasks(self):
        if self.tasks:
            for task in self.tasks.all():
                task.completion_date = now().date()
                super(Task, task).save()



'''
    def save(self, *args, **kwargs):
        if self.publish_date is None:
            self.publish_date = now()
        super(Update, self).save(*args, **kwargs)

    publish_date = models.DateTimeField(_("Publish Date"),
                                        help_text=_("The date of this project update, will default to now"),
                                        blank=True, null=True)

'''
