from django.urls import path
from . import views

urlpatterns = [
    path('portal/', views.dashboard, name='portal_dashboard'),
    path('portal/scores/', views.scores, name='portal_scores'),
]
