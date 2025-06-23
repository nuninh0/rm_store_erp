from django.urls import path
from . import views

urlpatterns = [
    path('', views.pdv, name='pdv'),
    path('adicionar-produto/', views.adicionar_produto_pdv, name='adicionar_produto_pdv'),
    path('remover-produto/<str:produto_codigo>/', views.remover_produto_pdv, name='remover_produto_pdv'),
    path('finalizar-venda/', views.finalizar_venda, name='finalizar_venda'),
    path('comprovante/<int:venda_id>/', views.comprovante_venda, name='comprovante_venda'),

]