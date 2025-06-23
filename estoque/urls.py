from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_estoque, name='lista_estoque'),
    path('editar/<int:pk>/', views.editar_estoque, name='editar_estoque'),
]