from django import forms
from django.shortcuts import render
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Fieldset, HTML, ButtonHolder, Submit
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab
from django.forms import inlineformset_factory
from django.template.loader import render_to_string
from crispy_forms.layout import LayoutObject, TEMPLATE_PACK

from . import models


class Formset(LayoutObject):
    template = "contabilidad/formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, context, template_pack=TEMPLATE_PACK, **kwargs):
        template = self.get_template_name(template_pack)
        formset = context[self.formset_name_in_context]
        return render_to_string(template, {'formset': formset})


class ConceptoEntradaForm(forms.ModelForm):
    class Meta:
        model = models.ConceptoEntrada
        exclude = ()


class ConceptoSalidaForm(forms.ModelForm):
    class Meta:
        model = models.ConceptoSalida
        exclude = ()


class EntradaForm(forms.ModelForm):

    class Meta:
        model = models.Entrada
        fields = ['fecha_pago', 'de', 'notas']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'id': 'datepicker'}),
            # 'de': forms.DateInput(attrs={'class': 'select form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(EntradaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-3 create-label'
        # self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Fieldset('Datos generales',
                         Row(
                             Column(Field('fecha_pago'),
                                    css_class='form-group col-md-4 mb-0'),
                             Column(Field('de', css_class="select-js"),
                                    css_class='form-group col mb-0'),
                         ),
                         ),
                # Field('fecha_pago'),
                # Field('de'),
                Fieldset('Conceptos del Entrada',
                         Formset('concepto')
                         ),
                Field('notas'),
                # Fieldset('Agregar documento',
                #          Formset('documento')),

                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Guardar')),
            )
        )


class SalidaForm(forms.ModelForm):

    class Meta:
        model = models.Salida
        fields = ['folio', 'proveedor', 'de', 'fecha_pago', 'notas']
        widgets = {
            'fecha_pago': forms.DateInput(attrs={'id': 'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(SalidaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-3 create-label'
        # self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Fieldset('Datos generales',
                         Row(
                             Column(Field('fecha_pago'),
                                    css_class='form-group col-md-4 mb-0'),
                             Column(Field('de', css_class="select-js"),
                                    css_class='form-group col-md-4 mb-0'),
                             Column(Field('folio'),
                                    css_class='form-group col-md-4 mb-0'),
                         ),
                         Row(
                             Field('proveedor'),
                         ),
                         ),
                # Field('folio'),
                # Field('proveedor'),
                # Field('fecha_pago'),
                Fieldset('Conceptos del Salida',
                         Formset('concepto')
                         ),
                Field('notas'),
                # Fieldset('Agregar documento',
                #          Formset('documento')),

                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Guardar')),
            )
        )


ConceptoEntradaFormSet = inlineformset_factory(
    models.Entrada, models.ConceptoEntrada, form=ConceptoEntradaForm,
    fields=['miembro',  'concepto', 'cuenta_contable', 'importe'], extra=2, can_delete=True
)

ConceptoSalidaFormSet = inlineformset_factory(
    models.Salida, models.ConceptoSalida, form=ConceptoSalidaForm,
    fields=['concepto', 'cuenta_contable', 'importe'], extra=1, can_delete=True
)
