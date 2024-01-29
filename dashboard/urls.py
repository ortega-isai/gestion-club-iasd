from django.urls import path, include
from .views import *

urlpatterns = [
    path('', DashboardTemplateView.as_view(),
         name='home'),
]
