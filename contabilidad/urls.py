from django.urls import path, include
from .views import *

urlpatterns = [
    # # Dashboard
    path('mensual', ContabilidadTemplateView.as_view(),
         name='contabilidad-mensual'),
    path('', ContabilidadAnualTemplateView.as_view(),
         name='contabilidad'),
    # entrada
    path('conceptopago', ConceptoEntradaListView.as_view(),
         name='conceptopago'),

    # entrada
    path('entradas', EntradasListView.as_view(),
         name='entradas'),
    path('entrada/<int:pk>', EntradaDetailView.as_view(),
         name='entrada-detail'),
    path('entrada/new/', EntradaCreateViews.as_view(),
         name='entrada-new'),

    # salidas
    path('salida', SalidasListView.as_view(),
         name='salidas'),
    path('salida/<int:pk>', SalidaDetailView.as_view(),
         name='salida-detail'),
    path('salida/new/', SalidaCreateViews.as_view(),
         name='salida-new'),
]
