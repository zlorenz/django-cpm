import json
from django.contrib.auth.models import User
from django.db.models import Q

from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.forms.models import inlineformset_factory
from braces.views import JSONResponseMixin

from .models import Message


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
                }
            return self.render_to_json_response(data)
        else:
            return response



class MessageListView(JSONResponseMixin, generic.ListView):
    model = Message
    content_type = 'application/javascript'
    json_dumps_kwargs = {'indent': 2}
    template_name = 'messages/message_list.html'


    def get(self, request, *arg, **kwargs):
        self.user = get_object_or_404(User, id=self.args[0])
        user_messages = Message.objects.filter(
            Q(user=self.user) | Q(recipient=self.user)
        ).order_by('created')

        if request.is_ajax():
            context = {}

            for message in user_messages:
                message_context = {
                    'message': message.message,
                    'created': message.created,
                    'user': message.user.username,
                    'recipient': message.recipient.username,
                }
                context[message.id] = message_context

            context.update(kwargs)
            return self.render_json_response(context)
        else:
            context = {'message_list': user_messages}
            return render(request, self.template_name, context)


class MessageDetailView(JSONResponseMixin, generic.DetailView):
    model = Message
    content_type = 'application/javascript'
    json_dumps_kwargs = {'indent': 2}
    template_name = 'messages/message_detail.html'

    def get(self, request, *arg, **kwargs):
        if request.is_ajax():
            context = {}
            context.update(kwargs)

            context += {
                'message': self.object.message,
                'created': self.object.created,
                'user': self.object.user,
                'recipient': self.object.recipient,
            }

            return self.render_json_response(context)
        else:
            context = {'message': self.get_object(self.get_queryset())}
            return render(request, self.template_name, context)


class MessageFormView(AjaxableResponseMixin, generic.CreateView):
    model = Message


class MessageUpdateView(AjaxableResponseMixin, generic.UpdateView):
    model = Message


class MessageDeleteView(generic.DeleteView):
    model = Message
    success_url = reverse_lazy('messages:message-list')
