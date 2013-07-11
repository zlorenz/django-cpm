from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User)
    recipient = models.ForeignKey(User, related_name='received_messages')
    message = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return str(self.created)

    def get_absolute_url(self):
        return reverse('messages:message-detail', kwargs={'pk': self.pk})


