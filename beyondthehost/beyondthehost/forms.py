from crispy_forms.helper import FormHelper

class HorizontalNoFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(HorizontalNoFormHelper, self).__init__(*args, **kwargs)
        self.form_class = 'form-horizontal'
        self.label_class = 'col-sm-2'
        self.field_class = 'col-sm-10'
        self.form_tag = False
        self.disable_csrf = True
