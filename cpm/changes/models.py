from django.db import models
from django.core.urlresolvers import reverse

from core.models import Slugged, base_concrete_model, DateStamp

from projects.models import Project

class ChangeOrder(DateStamp, Slugged):
    project = models.ForeignKey(Project)
    description = models.TextField(blank=True)
    publish_date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('changes:change-detail', kwargs={'pk': self.pk})


