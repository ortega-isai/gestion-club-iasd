from django import forms
from django.shortcuts import render
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Fieldset, HTML
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from .models import Miembro, Familia


class MiembroAddForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = '__all__'

        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'id': 'datepicker'}),
            # 'solicitante': forms.DateInput(attrs={'type': 'hidden'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset('Datos del miembro',
                     Row(
                         Column('nombre', css_class='form-group col-md-4 mb-0'),
                         Column('apellido_paterno',
                                css_class='form-group col-md-4 mb-0'),
                         Column('apellido_materno',
                                css_class='form-group col-md-4 mb-0'),
                     ),
                     Row(
                         Column('sexo', css_class='form-group col-md-4 mb-0'),
                         Column('fecha_nacimiento',
                                css_class='form-group col-md-4 mb-0'),
                         Column('familia',
                                css_class='form-group col-md-4 mb-0'),
                     ),
                     ),
            Fieldset('Datos del club',
                     Row(
                         Column('tipo_miembro',
                                css_class='form-group col-md-6 mb-0'),
                         Column('clase', css_class='form-group col-md-6 mb-0'),
                     ),
                     Field('miembro_iglesia'),

                     ),
        )
        self.helper.add_input(Submit('submit', 'Aceptar'))


class FamiliaAddForm(forms.ModelForm):
    class Meta:
        model = Familia
        fields = ['nombre_familia']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('nombre_familia'),
        )
        self.helper.add_input(Submit('submit', 'Aceptar'))
