from .utils import Calendar
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count
from . import models, forms
from django_pandas.io import read_frame
from django.db.models import Avg, Count, Min, Sum
import pandas as pd
import numpy as np


from datetime import datetime, date, timedelta
from django.utils.safestring import mark_safe
import calendar
calendar.setfirstweekday(calendar.SUNDAY)


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
