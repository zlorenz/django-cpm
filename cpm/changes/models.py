from django.db import models
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from core.models import Slugged, base_concrete_model, DateStamp

from cpm.projects.models import Project

class ChangeOrder(Slugged):
    project = models.ForeignKey(Project)
    description = models.TextField(blank=True)
    publish_date = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('changes:change-detail', kwargs={'pk': self.pk})


