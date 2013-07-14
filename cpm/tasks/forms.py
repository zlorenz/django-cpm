from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from django.forms.extras.widgets import SelectDateWidget

from tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'slug', 'description', 'projected_completion_date', 'project']
        widgets = {
            'slug': forms.HiddenInput(),
            'projected_completion_date': SelectDateWidget(),
            'completion_date': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.help_text_inline = True
        #self.helper.form_tag = False
        self.helper.form_id = 'task-update-form'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        Div(
                            'slug',
                            Field('title', css_class='span3', onchange='$("#task-update-form").submit()'),
                            #Field('status', css_class='span3'),
                            #Field('projected_completion_date', css_class='span1'),
                            #Field('project', css_class='span3'),
                            Field('status'),
                            Field('project'),
                            Field('projected_completion_date'),
                            css_class='span3',
                        ),
                        Div(
                            Field('description', css_class='span3'),
                            css_class='span3',
                        ),
                        css_class='row'
                    ),
                ),
            )
        )


