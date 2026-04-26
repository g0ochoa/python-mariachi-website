from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portal/media/', views.media_manager, name='media_manager'),
    path('portal/media/<str:slot>/upload/', views.media_upload, name='media_upload'),
    path('portal/media/<str:slot>/delete/', views.media_delete, name='media_delete'),
]
