from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.http import Http404
# from faker import Faker
from django_pandas.io import read_frame
import pandas as pd
import numpy as np
from datetime import datetime
from django.db.models import Avg, Count, Min, Sum
import calendar
from django.utils.translation import gettext

from . import forms
from club import models
from contabilidad import models

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardTemplateView,
                        self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)

        miembros = models.Miembro.objects.all()
        df_miembros = read_frame(miembros)

        df_miembros_count = df_miembros.groupby(
            ['tipo_miembro'])['tipo_miembro'].count().reset_index(name='counts').to_dict("index")
        context['tipo_miembro_count'] = df_miembros_count
        context['miembro_count'] = models.Miembro.objects.count()

        anio_actual = datetime.now().year
        mes_actual = datetime.now().month

        mes_nombre = calendar.month_name[mes_actual]

        recibos = models.Entrada.objects.filter(fecha_pago__year=anio_actual
                                                #    ,fecha_pago__month=mes_actual
                                                )
        conceptopago = models.ConceptoEntrada.objects.filter(
            entrada__in=recibos)

        gastos = models.Salida.objects.filter(fecha_pago__year=anio_actual
                                              #  ,fecha_pago__month=mes_actual
                                              )
        conceptogasto = models.ConceptoSalida.objects.filter(salida__in=gastos)

        context['mes_nombre'] = mes_nombre

        context['entrada_mes_actual_importe'] = conceptopago.aggregate(
            Sum('importe'))
        context['salidas_mes_actual_importe'] = conceptogasto.aggregate(
            Sum('importe'))

        context['entradas_mes_actual_conteo'] = conceptopago.count()
        context['salidas_mes_actual_conteo'] = conceptogasto.count()

        suma_egreso = conceptogasto.aggregate(Sum('importe'))['importe__sum']
        suma_ingreso = conceptopago.aggregate(Sum('importe'))['importe__sum']

        if (suma_egreso is None):
            suma_egreso = 0

        if (suma_ingreso is None):
            suma_ingreso = 0
        context['saldo'] = suma_ingreso - suma_egreso
        return context


class ReportesTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/reportes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PagosConceptoTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/reportes/reporte_pagoconcepto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pagos = models.ConceptoEntrada.objects.all()
        df = read_frame(pagos)
        pivote_table = pd.pivot_table(
            df,
            index=['miembro', ],
            columns=['concepto', ],
            values=['importe'],
            aggfunc=np.sum,
            fill_value='',
            margins=True,
            margins_name='Total',
        )

        context['resultado'] = pivote_table.to_html(
            classes=["table", "table-sm", "table-striped",
                     "table-bordered"],
            border=0,
            # table_id='dataTable',
            float_format='${:,.2f}'.format,
            index=True
        )

        return context


class CuotasTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/reportes/reporte_cuotas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pagos = models.ConceptoEntrada.objects.filter(
            concepto__concepto__contains="Cuota")
        df = read_frame(pagos)
        # n_by_state = df.groupby("state")["last_name"].count()

        pivote_table = pd.pivot_table(
            df,
            index=['miembro', ],
            columns=['concepto', ],
            values=['importe'],
            aggfunc=np.sum,
            fill_value='',
            margins=True,
            margins_name='Total',
        )

        context['resultado'] = pivote_table.to_html(
            classes=["table", "table-sm", "table-striped",
                     "table-bordered"],
            border=0,
            # table_id='dataTable',
            float_format='${:,.2f}'.format,
            index=True
        )

        return context


class CamporeeTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/reportes/reporte_cuotas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pagos = models.ConceptoEntrada.objects.filter(
            concepto__concepto__contains="Camporee"
        ).values(
            'id', 'Recibo', 'miembro', 'miembro__tipo_miembro', 'miembro__clase', 'concepto', 'importe')

        df = read_frame(pagos, fieldnames=[
                        'id', 'Recibo', 'miembro', 'miembro__tipo_miembro', 'miembro__clase', 'concepto', 'importe'])

        # n_by_state = df.groupby("state")["last_name"].count()

        pivote_table = pd.pivot_table(
            df,
            index=['miembro__clase', 'miembro__tipo_miembro', 'miembro', ],
            columns=['concepto', ],
            values=['importe'],
            aggfunc=np.sum,
            fill_value='',
            margins=True,
            margins_name='Total',
        )

        context['resultado'] = pivote_table.to_html(
            classes=["table", "table-sm", "table-striped",
                     "table-bordered"],
            border=0,
            # table_id='dataTable',
            float_format='${:,.2f}'.format,
            index=True
        )

        return context


@login_required
def reporte_mensual_pagos(request):
    context = {}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.ReporteMensualPagoForm(
            request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            recibos = models.Entrada.objects.filter(fecha_pago__year=form.cleaned_data['anio'],
                                                    fecha_pago__month=form.cleaned_data['mes'])
            conceptopago = models.ConceptoEntrada.objects.filter(
                Recibo__in=recibos)

            df = read_frame(conceptopago)
            pivote_table = pd.pivot_table(
                df,
                index=['miembro', ],
                columns=['concepto', ],
                values=['importe'],
                aggfunc=np.sum,
                fill_value='',
                margins=True,
                margins_name='Total',
            )

            context['resultado'] = pivote_table.to_html(
                classes=["table", "table-sm", "table-striped",
                         "table-bordered"],
                border=0,
                # table_id='dataTable',
                float_format='${:,.2f}'.format,
                index=True
            )

            return render(request, 'dashboard/reportes/reporte_pagomensual.html', context)
    # if a GET (or any other method) we'll create a blank form
    else:
        form = forms.ReporteMensualPagoForm(
            initial={
                "anio": datetime.now().date().year,
                "mes": datetime.now().date().month
            }
        )
        context['form'] = form
        return render(request, 'generic_form.html', context)


class RecoleccionTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/reportes/reporte_recoleccion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pagos = models.ConceptoEntrada.objects.filter(
            concepto__concepto__contains="Recoleccion")

        # print(pagos)
        df = read_frame(pagos)
        df2 = df.groupby("miembro")["importe"].sum().reset_index('miembro')
        # print(df2)

        df2['porcentaje'] = df2['importe'] * 100 / 200
        df2 = df2.round(2)

        # print(df2.columns)
        # print(df2.to_dict('records'))
        context['recoleccion_list'] = df2.to_dict('records')
        pivote_table = pd.pivot_table(
            df,
            index=['miembro', ],
            columns=['concepto', ],
            values=['importe'],
            aggfunc=np.sum,
            fill_value='',
            margins=True,
            margins_name='Total',
        )

        context['resultado'] = pivote_table.to_html(
            classes=["table", "table-sm", "table-striped",
                     "table-bordered"],
            border=0,
            # table_id='dataTable',
            float_format='${:,.2f}'.format,
            index=True
        )

        return context
