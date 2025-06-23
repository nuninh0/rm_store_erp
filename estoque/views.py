from django.shortcuts import render, redirect, get_object_or_404
from .models import Estoque
from django.db.models import F #para operações de banco de dados mais seguras 
from .forms import EstoqueForm

# Create your views here.
def lista_estoque(request):
    #.select_related('produto') otimiza a consulta, buscando o dados do produto
    #relacionando na mesma query, evitando consultas extras no loop do template
    estoques = Estoque.objects.select_related('produto').filter(produto__ativo=True).order_by('produto__nome')
    return render(request, 'estoque/lista_estoque.html', {'estoques': estoques})

def editar_estoque(request, pk):
    #aqui, o 'pk' é da tabela Estoque, não do produto.
    estoque_item = get_object_or_404(Estoque, pk=pk)

    if request.method == 'POST':
        form = EstoqueForm(request.POST, instance=estoque_item)
        if form.is_valid():
            form.save()
            return redirect('lista_estoque')
    else:
        form = EstoqueForm(instance=estoque_item)

    return render(request, 'estoque/editar_estoque.html', {
        'form': form,
        'produto_nome': estoque_item.produto.nome
    })