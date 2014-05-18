from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Button, Fieldset
from crispy_forms.bootstrap import FormActions


class AppForm(forms.Form):
    app_type = forms.ChoiceField(choices=(('wordpress', 'Wordpress'),
                                          ('static', 'Static HTML/PHP'),)
                                )
    name = forms.CharField(help_text='Any name')
    
    def __init__(self, *args, **kwargs):
        super(AppForm, self).__init__(*args, **kwargs)
        helper = FormHelper()
        
        #helper.form_class = 'form-horizontal'
        #helper.label_class = 'col-lg-2'
        #helper.field_class = 'col-lg-6'
        helper.layout = Layout(
            'name',
            'app_type', 
            FormActions(
                Submit('next', 'Next'),
            ),
        )
        
        self.helper = helper