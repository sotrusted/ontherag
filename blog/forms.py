from django import forms
from filer.fields.image import FilerImageField
from crispy_forms.helper import FormHelper
from .models import Personal, Images
from crispy_forms.layout import Layout, Submit, Div, Field, HTML, Row, Column


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleImageField(FilerImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleImageInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result        

class MultipleImageField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name    

class PersonalForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100, 
        label='what are you looking for?'
        )
    
    city = forms.CharField(
        max_length=100, 
        label='city or neighborhood',
        required=False
        )
    
    description = forms.CharField(
        widget=forms.Textarea, 
        label='description'
        )
#    images = MultipleImageField(
 #       label='pics', 
  #      required=False
   # )

    image1 = forms.ImageField(required=False, label='')
    image2 = forms.ImageField(required=False, label='')
    image3 = forms.ImageField(required=False, label='')
    image4 = forms.ImageField(required=False, label='')
    image5 = forms.ImageField(required=False, label='')
    image6 = forms.ImageField(required=False, label='')

    phone = forms.CharField(
        max_length=20, 
        label='phone', 
        required=False
        )
    
    email = forms.EmailField(
        label='email', 
        required=False
        )
    
    social_link = forms.URLField(
        label='social', 
        required=False
        )

    class Meta:
        model = Personal
        fields = ('title', 'city', 'description', 'image', \
                  'phone', 'email', 'social_link' )


    def __init__(self, *args, **kwargs):
        super(PersonalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        
        self.helper.layout = Layout(
            Div(
                HTML('<legend class="outer-legend">post a personal</legend>'),
                Row(
                    Column('title', css_class='form-group col-md-6 mb-0'),
                    Column('city', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('description', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('image1', css_class='form-group col-md-4 mb-0 custom-image-field'),
                    Column('image2', css_class='form-group col-md-4 mb-0 custom-image-field'),
                    Column('image3', css_class='form-group col-md-4 mb-0 custom-image-field'),
                    css_class='form-row'
                ),
                Row(
                    Column('image4', css_class='form-group col-md-4 mb-0 custom-image-field'),
                    Column('image5', css_class='form-group col-md-4 mb-0 custom-image-field'),
                    Column('image6', css_class='form-group col-md-4 mb-0 custom-image-field'),
                    css_class='form-row'
                ),
                Div(
                    HTML('<legend class="inner-legend"><span>contact</span></legend>'),
                    Field('phone'),
                    Field('email'),
                    Field('social_link'),
                    css_class='personal-form-inner'
                ),
                css_class="personal-form-outer"
            ),
            Submit('submit', 'Submit'),
        )

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image', required=False)
    
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(
            Field('image', css_class='formset_row', required=False)
        )

    class Meta:
        model = Images
        fields = ('image', )
        

class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(
            Div(
                HTML('<legend class="inner-legend"><span>contact</span></legend>'),
                Field('phone'),
                Field('email'),
                Field('social_link'),
                css_class='personal-form-inner'
            ),
            Submit('submit', 'Submit'),
        )
    class Meta:
        model = Personal
        fields =   ('phone', 'email', 'social_link' )

'''
                Row(
                    Column('images', css_class='form-group col-md-12 mb-0 custom-image-field'),
                    css_class='form-row'
                ),
'''
