from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from .models import Venda, ItemVenda
from produtos.models import Produto
from estoque.models import Estoque


# Create your views here.

def pdv(request):
    #O carrinho é armazenado na sessão de Django
    carrinho_session = request.session.get('carrinho', {})

    #NOva lista de itens para o template, com mais templates 
    carrinho_context = []
    valor_total = 0

    for codigo, item_session in carrinho_session.items():
        quantidade = item_session['quantidade']
        preco = float(item_session['preco'])
        subtotal = preco * quantidade

        carrinho_context.append({
            'codigo' : codigo,
            'nome': item_session['nome'],
            'quantidade': quantidade,
            'preco': preco,
            'subtotal': subtotal
        })

        valor_total += subtotal

    formas_pagamento = Venda.FORMAS_PAGAMENTO

    context = {
        'carrinho': carrinho_context, # usamos a nova lista
        'valor_total': valor_total,
        'formas_pagamento': formas_pagamento
    }
    return render(request, 'vendas/pdv.html', context)

def adicionar_produto_pdv(request):
    if request.method == 'POST':
        codigo_produto = request.POST.get('codigo_produto')
        quantidade = int(request.POST.get('quantidade', 1))

        try:
            produto = Produto.objects.get(codigo=codigo_produto, ativo=True)
            estoque=Estoque.objects.get(produto=produto)

            if estoque.quantidade < quantidade:
                messages.error(request, f"Estoque insuficiente para'{produto.nome}'. Disponível: {estoque.quantidade}")
                return redirect('pdv')
            
            carrinho = request.session.get('carrinho', {})

            #se o produto já esta no carrinho, soma a quantidade 
            if codigo_produto in carrinho:
                carrinho[codigo_produto]['quantidade'] += quantidade
            else:
                carrinho[codigo_produto] = {
                    'nome': produto.nome,
                    'preco': str(produto.preco), #decimal precisa ser convertido
                    'quantidade': quantidade,
                    'codigo': produto.codigo,
                }
            request.session['carrinho']= carrinho
            messages.success(request, f"'{produto.nome}' adicionado ao carrinho.")
        except Produto.DoesNotExist:
            messages.error(request, f"Produto com código '{codigo_produto} não encontrado.")
    return redirect('pdv')


def remover_produto_pdv(request, produto_codigo):
    carrinho = request.session.get('carrinho', {})
    if produto_codigo in carrinho:
        del carrinho[produto_codigo]
        request.session['carrinho'] = carrinho
        messages.info(request, "Produto removido do carrinho.")
    return redirect('pdv')


@transaction.atomic
def finalizar_venda(request):
    if request.method == 'POST':
        carrinho = request.session.get('carrinho', {})
        if not carrinho:
            messages.error(request, "O carrinho está vazio.")
            return redirect('pdv')
        
        forma_pagamento = request.POST.get('forma_pagamento')
        valor_total = sum(float(item['preco']) * item['quantidade'] for item in carrinho.values())

        # 1. Cria o registro da venda 
        venda = Venda.objects.create(
            valor_total=valor_total,
            forma_pagamento=forma_pagamento
        )

        #2. Cria os itens da venda e atualiza o estoque
        for codigo, item in carrinho.items():
            produto = Produto.objects.get(codigo=codigo)

            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=item['quantidade'],
                preco_unitario=item['preco']
            )
        
        #3. Dá baixa no estoque
            estoque =Estoque.objects.get(produto=produto)
            estoque.quantidade -= item['quantidade']
            estoque.save()

    #4. Limpa o carrinho da sessão
        del request.session['carrinho']

        messages.success(request, f"Venda #{venda.pk} finalizada com sucesso!")
        return redirect('comprovante_venda', venda_id=venda.pk)

    return redirect('pdv')


def comprovante_venda(request, venda_id):
    venda = get_object_or_404(Venda, pk=venda_id)
    #usamos o 'related_name' que definimos no modelo para pegar 
    itens = venda.itens.all()

    context = {
        'venda': venda,
        'itens': itens,
    }
    return render(request, 'vendas/comprovante.html', context)