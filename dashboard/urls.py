from django.urls import path, include
from .views import *

urlpatterns = [
    path('', DashboardTemplateView.as_view(),
         name='home'),
    path('reportes', ReportesTemplateView.as_view(),
         name='reportes'),
         
    path('reportes/reporte-pagos-conceptos', PagosConceptoTemplateView.as_view(),
         name='reporte-pagos-conceptos'),
    path('reportes/reporte-pagos-cuotas', CuotasTemplateView.as_view(),
         name='reporte-pagos-cuotas'),
    path('reportes/reporte-pagos-camporee', CamporeeTemplateView.as_view(),
         name='reporte-pagos-camporee'),
    path('reportes/reporte_mensual_pagos', reporte_mensual_pagos,
         name='reporte_mensual_pagos'),
    path('reportes/reporte-recoleccion', RecoleccionTemplateView.as_view(),
         name='reporte-recoleccion'),
]
