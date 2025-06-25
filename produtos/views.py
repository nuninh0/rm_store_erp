from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Produto
from .forms import ProdutoForm

# Create your views here.
@login_required
def lista_produtos(request):
    produtos = Produto.objects.filter(ativo=True).order_by('nome') # busca todos os produtos 
    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos})
#view para criar um novo produto
@login_required
def novo_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()#salva o novo produto no banco de dados
            return redirect('lista_produtos') # redireciona para a lista
    else:
        form = ProdutoForm()
    return render(request, 'produtos/produto_form.html', {'form': form})
@login_required
#View para editar um produto existente(Update)
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form =ProdutoForm(instance=produto)
    return render(request, 'produtos/produto_form.html', {'form': form, 'produto': produto})
@login_required
#View para excluir um produto
def desativar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method =='POST':
        produto.ativo = False
        produto.save()
        return redirect('lista_produtos')
    return render(request, 'produtos/produto_confirm_delete.html', {'produto': produto})