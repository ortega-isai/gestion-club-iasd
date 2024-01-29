from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ClubDashboard.as_view(),
         name='miembros'),
    path('miembros', MiembrosListView.as_view(),
         name='miembros-list'),
    path('<int:pk>', MiembroDetailView.as_view(),
         name='miembro-detail'),
    path('<int:pk>/', MiembroUpdateView.as_view(),
         name='miembro-update'),
    path('new/', MiembroCreateView.as_view(),
         name='miembro-new'),

    path('calendar-cumple', CalendarioCumples.as_view(), name='calendar-cumple'),

    path('familia/New/', FamiliaCreateView.as_view(),
         name='familia-new'),
    path('familia/<int:pk>', FamiliaDetailView.as_view(),
         name='familia-detail'),
]
