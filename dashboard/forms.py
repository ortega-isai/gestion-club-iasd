from django import forms
from django.shortcuts import render
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Fieldset, HTML
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab


class ReporteMensualPagoForm(forms.Form):
    # CHOICES
    ENERO = 1
    FEBRERO = 2
    MARZO = 3
    ABRIL = 4
    MAYO = 5
    JUNIO = 6
    JULIO = 7
    AGOSTO = 8
    SEPTIEMBRE = 9
    OCTUBRE = 10
    NOVIEMBRE = 11
    DICIEMBRE = 12

    MESES_CHOICES = (
        (ENERO, '01 - ENERO'),
        (FEBRERO, '02 - FEBRERO'),
        (MARZO, '03 - MARZO'),
        (ABRIL, '04 - ABRIL'),
        (MAYO, '05 - MAYO'),
        (JUNIO, '06 - JUNIO'),
        (JULIO, '07 - JULIO'),
        (AGOSTO, '08 - AGOSTO'),
        (SEPTIEMBRE, '09 - SEPTIEMBRE'),
        (OCTUBRE, '10 - OCTUBRE'),
        (NOVIEMBRE, '11 - NOVIEMBRE'),
        (DICIEMBRE, '12 - DICIEMBRE'),
    )
    anio = forms.IntegerField(
        min_value=2019,
        label='Año'
    )
    mes = forms.ChoiceField(
        choices=MESES_CHOICES,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('''
            <h3>Selecciona un mes en particular para revisar</h3>
            <p>
            Selecciona un año y un mes en particular para revisar
            los pagos que se han realizado durante el mes seleccionado
            </p>
            '''),
            Field('anio'),
            Field('mes'),
        )
        self.helper.add_input(Submit('submit', 'Aceptar'))


# class PermisoEspecialForm(forms.Form):
#     roles = forms.MultipleChoiceField()
#     nominas = forms.MultipleChoiceField()
#     # user = forms.ModelChoiceField(
#     #     queryset=CustomUser.objects.all(),
#     #     widget=forms.HiddenInput()
#     # )

#     roles.widget.attrs.update(size='10')
#     nominas.widget.attrs.update(size='10')

#     def __init__(self, ambiente, *args, **kwargs):
#         super(PermisoEspecialForm, self).__init__(*args, **kwargs)
#         rol = lista_rol_ambiente_choices(ambiente)
#         elementos = lista_elementopermiso_ambiente_choices(ambiente)
#         self.fields['roles'].choices = rol
#         self.fields['nominas'].choices = elementos
#         # self.fields['tipo_apertura'].label = "Tipo de apertura"
#         self.helper = FormHelper()
#         self.helper.add_input(
#             Submit('submit', 'Aceptar', css_class='btn-success'))
