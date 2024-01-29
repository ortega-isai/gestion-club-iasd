from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MiembrosListView.as_view(),
         name='miembros'),
    path('miembros', MiembrosListView.as_view(),
         name='miembros-list'),
    path('<int:pk>', MiembroDetailView.as_view(),
         name='miembro-detail'),
    path('<int:pk>/', MiembroUpdateView.as_view(),
         name='miembro-update'),
    path('new/', MiembroCreateView.as_view(),
         name='miembro-new'),

]
