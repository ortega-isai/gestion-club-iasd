from .utils import Calendar
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count
from . import models, forms
from contabilidad.models import Entrada, ConceptoEntrada
from django_pandas.io import read_frame
from django.db.models import Avg, Count, Min, Sum
import pandas as pd
import numpy as np


from datetime import datetime, date, timedelta
from django.utils.safestring import mark_safe
import calendar
calendar.setfirstweekday(calendar.SUNDAY)


class ClubDashboard(PermissionRequiredMixin, TemplateView):
    permission_required = 'club.view_miembro'
    template_name = 'club/miembro_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        familias = models.Familia.objects.all()
        context['familia_list'] = familias
        miembros = models.Miembro.objects.all()
        context['miembro_count'] = models.Miembro.objects.count()

        df_miembros = read_frame(miembros, fieldnames=['id', 'nombre', 'apellido_paterno', 'apellido_materno',
                                                       'fecha_nacimiento', 'sexo', 'familia', 'tipo_miembro', 'clase',
                                                       'clase__hexcolor', 'miembro_iglesia',])

        # por tipo de miembro
        df_tipo_miembro_count = df_miembros.groupby(
            ['tipo_miembro'])['tipo_miembro'].count().reset_index(name='counts').to_dict("index")
        context['tipo_miembro_count'] = df_tipo_miembro_count

        # por clase de miembro
        df_clase_miembro_count = df_miembros.groupby(['clase', 'clase__hexcolor'])[
            'clase'].count().reset_index(name='counts').to_dict("index")
        context['clase_miembro_count'] = df_clase_miembro_count

        # por tipo - clase de miembro
        df_general_miembro_count = df_miembros.groupby(['tipo_miembro', 'clase', 'clase__hexcolor', ])[
            'clase'].count().reset_index(name='counts').to_dict("index")
        context['general_miembro_count'] = df_general_miembro_count

        # print(df_general_miembro_count)

        return context


class MiembrosListView(PermissionRequiredMixin, ListView):
    permission_required = 'club.view_miembro'
    model = models.Miembro


class MiembroDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'club.view_miembro'
    model = models.Miembro


class MiembroUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'club.change_miembro'
    model = models.Miembro
    form_class = forms.MiembroAddForm
    template_name = r'generic_form.html'


class MiembroCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'club.add_miembro'
    model = models.Miembro
    form_class = forms.MiembroAddForm
    template_name = r'generic_form.html'


class FamiliaCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'club.add_familia'
    model = models.Familia
    form_class = forms.FamiliaAddForm
    template_name = r'generic_form.html'

    def get_success_url(self):
        return reverse_lazy('miembros')


class FamiliaDetailView(PermissionRequiredMixin, DetailView):
    permission_required = 'club.view_familia'
    model = models.Familia

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        familia = self.object
        recibo = Entrada.objects.filter(
            de__in=familia.miembro_set.all()
        )
        # recibo = Recibo.objects.filter(
        #     recibos__miembro__in=familia.miembro.all()
        # )
        conceptopago = ConceptoEntrada.objects.filter(
            miembro__in=familia.miembro_set.all()
        )

        context['importe_total'] = conceptopago.aggregate(
            Sum('importe'))
        context['id_count'] = conceptopago.count()
        if conceptopago:
            df = read_frame(conceptopago)
            pivote_table = pd.pivot_table(
                df,
                index=['concepto', ],
                columns=['miembro', ],
                values=['importe'],
                aggfunc=np.sum,
                fill_value='',
                margins=True,
                margins_name='Total',
            )

            context['reporte_conceptos'] = pivote_table.to_html(
                classes=["table", "table-sm", "table-striped",
                         "table-bordered"],
                border=0,
                # table_id='dataTable',
                float_format='${:,.2f}'.format,
                index=True
            )

        context['conceptopago_list'] = conceptopago
        context['recibo_list'] = recibo
        return context


class CalendarioCumples(LoginRequiredMixin, TemplateView):
    template_name = 'club/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
