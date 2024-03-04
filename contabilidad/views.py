from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView, TemplateView
from django.forms import inlineformset_factory
from django.db.models import Avg, Count, Min, Sum
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import calendar
from django.urls import reverse, reverse_lazy
from django.db import transaction
from . import models, forms
from django_pandas.io import read_frame
import pandas as pd
import numpy as np

from django.utils.formats import date_format
from django.utils import translation
from django.utils.translation import gettext
translation.activate('es')

# Views para el dashboard


class ContabilidadAnualTemplateView(PermissionRequiredMixin, TemplateView):
    template_name = r'contabilidad/contabilidad_anual.html'
    permission_required = [
        "contabilidad.view_entrada", "contabilidad.view_salida"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('anio'):
            anio_actual = int(self.request.GET.get('anio'))
        else:
            anio_actual = datetime.now().year

        entradas = models.ConceptoEntrada.objects.filter(
            entrada__fecha_pago__year=anio_actual,)
        salidas = models.ConceptoSalida.objects.filter(
            salida__fecha_pago__year=anio_actual,)

        anual = {}
        saldo_inicial = 0.00
        saldo_final = 0.00
        for mes in range(1, 13):
            # print(mes, end=", ")

            saldo_inicial = saldo_final
            mes_entrada = entradas.filter(
                entrada__fecha_pago__month=mes,
            ).aggregate(Sum('importe'))['importe__sum']
            mes_salida = salidas.filter(
                salida__fecha_pago__month=mes,
            ).aggregate(Sum('importe'))['importe__sum']
            if (mes_entrada is None):
                mes_entrada = 0.0
            if (mes_salida is None):
                mes_salida = 0.0
            saldo_final = saldo_inicial + mes_entrada - mes_salida
            anual[mes] = {
                "mes_nombre": gettext(calendar.month_name[mes]),
                "saldo_inicial": round(saldo_inicial, 2),
                "mes_entrada": round(mes_entrada, 2),
                "mes_salida": round(mes_salida, 2),
                "saldo_final": round(saldo_final, 2),
            }

        # print(anual)
        context['tabla_anual'] = anual

        context['pagos_anual_importe'] = entradas.aggregate(
            Sum('importe'))
        context['salidas_anual_importe'] = salidas.aggregate(
            Sum('importe'))

        context['pagos_anual_conteo'] = entradas.count()
        context['salidas_anual_conteo'] = salidas.count()

        suma_egreso = salidas.aggregate(Sum('importe'))['importe__sum']
        suma_ingreso = entradas.aggregate(Sum('importe'))['importe__sum']

        if (suma_egreso is None):
            suma_egreso = 0

        if (suma_ingreso is None):
            suma_ingreso = 0

        context['saldo'] = suma_ingreso - suma_egreso

        context['calendario'] = {
            'anio': anio_actual,
        }

        data_grafica = {"salidas": {}, "entradas": {},
                        "saldo_final": {}, "meses": []}
        for key, mes in anual.items():
            data_grafica['meses'].append(mes["mes_nombre"])
            data_grafica['salidas'][mes["mes_nombre"]] = mes['mes_salida']
            data_grafica['entradas'][mes["mes_nombre"]] = mes['mes_entrada']
            data_grafica['saldo_final'][mes["mes_nombre"]] = mes['saldo_final']

        data01 = {
            "labels": data_grafica['meses'],
            "salidas": data_grafica['salidas'],
            "entradas": data_grafica['entradas'],
            "saldo_final": data_grafica['saldo_final'],
        }
        context['data01'] = data01

        return context


class ContabilidadTemplateView(PermissionRequiredMixin, TemplateView):
    template_name = r'contabilidad/contabilidad.html'
    permission_required = [
        "contabilidad.view_entrada", "contabilidad.view_salida"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('mes'):
            mes_actual = int(self.request.GET.get('mes'))
        else:
            mes_actual = datetime.now().month

        if self.request.GET.get('anio'):
            anio_actual = int(self.request.GET.get('anio'))
        else:
            anio_actual = datetime.now().year

        mes_nombre = gettext(calendar.month_name[mes_actual])
        first_day, day_count = calendar.monthrange(anio_actual, mes_actual)

        entradas = models.Entrada.objects.filter(fecha_pago__year=anio_actual)
        salidas = models.Salida.objects.filter(fecha_pago__year=anio_actual)

        # ------------ Lista Entradas ------------

        entradas_del_mes = entradas.filter(fecha_pago__month=mes_actual)
        context['entradas_list'] = entradas_del_mes

        # ------------ lista Salidas ------------
        salidas_del_mes = salidas.filter(fecha_pago__month=mes_actual)
        context['salidas_list'] = salidas_del_mes

        # ------------ KPI Saldo anterior ------------

        ingresos_anterior = models.ConceptoEntrada.objects.filter(
            entrada__fecha_pago__year=anio_actual,
            entrada__fecha_pago__month__range=(1, mes_actual-1)
        ).aggregate(Sum('importe'))

        if (ingresos_anterior['importe__sum'] is None):
            ingresos_anterior['importe__sum'] = 0

        egresos_anterior = models.ConceptoSalida.objects.filter(
            salida__fecha_pago__year=anio_actual,
            salida__fecha_pago__month__range=(1, mes_actual-1),
        ).aggregate(Sum('importe'))

        if (egresos_anterior['importe__sum'] is None):
            egresos_anterior['importe__sum'] = 0

        saldo_anterior = ingresos_anterior['importe__sum'] - \
            egresos_anterior['importe__sum']

        context['pagos_anteriores_importe'] = saldo_anterior
        # ------------ KPI Entradas mes acutal ------------

        conceptopago_del_mes = models.ConceptoEntrada.objects.filter(
            entrada__in=entradas_del_mes)
        context['pagos_mes_actual_importe'] = conceptopago_del_mes.aggregate(
            Sum('importe'))
        context['pagos_mes_actual_conteo'] = conceptopago_del_mes.count()
        suma_ingreso = conceptopago_del_mes.aggregate(Sum('importe'))[
            'importe__sum']
        if (suma_ingreso is None):
            suma_ingreso = 0
        # ------------ KPI Salidas mes acutal ------------

        conceptosalida_del_mes = models.ConceptoSalida.objects.filter(
            salida__in=salidas_del_mes)
        context['salidas_mes_actual_importe'] = conceptosalida_del_mes.aggregate(
            Sum('importe'))
        context['salidas_mes_actual_conteo'] = conceptosalida_del_mes.count()
        suma_egreso = conceptosalida_del_mes.aggregate(Sum('importe'))[
            'importe__sum']
        if (suma_egreso is None):
            suma_egreso = 0

        # ------------ KPI saldo mes acutal ------------
        context['saldo'] = saldo_anterior + suma_ingreso - suma_egreso

        context['calendario'] = {
            'mes': mes_actual,
            'mes_nombre': mes_nombre,
            'anio': anio_actual,
            'first_day': first_day,
            'day_count': day_count,
        }
        return context


class ConceptoEntradaListView(PermissionRequiredMixin, ListView):
    permission_required = 'contabilidad.view_conceptoentrada'
    model = models.ConceptoEntrada

# Views para Entradas


class EntradasListView(PermissionRequiredMixin, ListView):
    permission_required = 'contabilidad.view_entrada'
    model = models.Entrada


class EntradaDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'contabilidad.view_entrada'
    model = models.Entrada


class EntradaCreateViews(PermissionRequiredMixin, CreateView):
    permission_required = 'contabilidad.add_entrada'
    model = models.Entrada
    template_name = 'contabilidad/entrada_form.html'
    form_class = forms.EntradaForm

    def get_context_data(self, **kwargs):
        data = super(EntradaCreateViews,
                     self).get_context_data(**kwargs)
        if self.request.POST:
            data['concepto'] = forms.ConceptoEntradaFormSet(self.request.POST)
            # data['documento'] = DocumentacionFormSet(self.request.POST, self.request.FILES)
        else:
            data['concepto'] = forms.ConceptoEntradaFormSet()
            # data['documento'] = DocumentacionFormSet()
        return data

    # def get_success_url(self):
    #     return reverse('solicitud-pdf-view', args=(self.object.id,))

    def form_valid(self, form):
        context = self.get_context_data()
        concepto = context['concepto']
        # documento = context['documento']
        with transaction.atomic():
            self.object = form.save()
            if concepto.is_valid():
                concepto.instance = self.object
                concepto.save()
            # if documento.is_valid():
            #     documento.instance = self.object
            #     documento.save()
        return super(EntradaCreateViews, self).form_valid(form)

# Views para Salidas


class SalidasListView(PermissionRequiredMixin, ListView):
    permission_required = 'contabilidad.view_salida'
    model = models.Salida


class SalidaDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'contabilidad.view_salida'
    model = models.Salida


class SalidaCreateViews(PermissionRequiredMixin, CreateView):
    permission_required = 'contabilidad.add_salida'
    model = models.Salida
    template_name = 'contabilidad/salida_form.html'
    form_class = forms.SalidaForm

    def get_context_data(self, **kwargs):
        data = super(SalidaCreateViews,
                     self).get_context_data(**kwargs)
        if self.request.POST:
            data['concepto'] = forms.ConceptoSalidaFormSet(self.request.POST)
            # data['documento'] = DocumentacionFormSet(self.request.POST, self.request.FILES)
        else:
            data['concepto'] = forms.ConceptoSalidaFormSet()
            # data['documento'] = DocumentacionFormSet()
        return data

    # def get_success_url(self):
    #     return reverse('solicitud-pdf-view', args=(self.object.id,))

    def form_valid(self, form):
        context = self.get_context_data()
        concepto = context['concepto']
        # documento = context['documento']
        with transaction.atomic():
            self.object = form.save()
            if concepto.is_valid():
                concepto.instance = self.object
                concepto.save()
            # if documento.is_valid():
            #     documento.instance = self.object
            #     documento.save()
        return super(SalidaCreateViews, self).form_valid(form)
