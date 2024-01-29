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
# from contabilidad import models

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

        return context
