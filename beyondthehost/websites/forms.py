from django import forms


class URLForm(forms.Form):
    url = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        super(URLForm, self).__init__(*args, **kwargs)

        helper = FormHelper()        
        helper.form_class = 'form-horizontal'
        #helper.label_class = 'col-lg-2'
        #helper.field_class = 'col-lg-6'
        helper.layout = Layout(
            'domains',
            FormActions(
                Submit('next', 'Next'),
            ),
        )
        self.helper = helper
