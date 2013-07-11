from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from core.models import Slugged, base_concrete_model, DateStamp


class Project(Slugged):
    user = models.ForeignKey(User, blank=True)
    #description
    #blueprints
    #drawings

    def get_absolute_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.pk})
