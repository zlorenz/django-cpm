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

