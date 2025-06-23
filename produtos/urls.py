from django.urls import path 
from . import views

urlpatterns = [
    #rota para a lista de produtos (read)
    path('', views.lista_produtos, name='lista_produtos'),
    #rota para o formulário de novo produto (create)
    path('novo', views.novo_produto, name='novo_produto'),
    #rota para editar um produto
    path('<int:pk>/editar/', views.editar_produto, name='editar_produto'),
    #rota para excluir um produto
    path('<int:pk>/desativar/', views.desativar_produto, name='desativar_produto'),
]