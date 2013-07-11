from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms import bootstrap
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.forms.extras.widgets import SelectDateWidget

from .models import Update


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Update
        exclude = ('project',)
