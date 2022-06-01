from crispy_forms.helper import FormHelper

# 基本的FormHelper
class BaseFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(BaseFormHelper, self).__init__(*args, **kwargs)
        self.form_method = "POST"
        self.form_class = "blueForms"
        self.form_class = "form-horizontal"
        self.label_class = "col-lg-2"
        self.field_class = "col-lg-8"
        # self.label_class = "col-sm-12 col-md-12 col-lg-12"
        # self.field_class = "col-sm-12 offset-md-2 col-md-8 offset-lg-2 col-lg-8"
