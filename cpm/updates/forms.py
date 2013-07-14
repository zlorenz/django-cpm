from django import forms

from .models import Update


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Update
        exclude = ('project',)
