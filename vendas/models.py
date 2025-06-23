from django.db import models
from produtos.models import Produto

# Create your models here.
class Venda(models.Model):
    FORMAS_PAGAMENTO = [
        ('PIX', 'Pix'),
        ('CD', 'Cartão de Débito'),
        ('PIX', 'Cartão de Crédito'),
        ('DIN', 'Dinheiro'),
    ]
    data = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2) 
    forma_pagamento = models.CharField(max_length=3, choices=FORMAS_PAGAMENTO)

    def __str__(self):
        #formatar a data para o fuso horario local (opcional, mas bom para visual)
        data_local = self.data.strftime('%d/%m/%Y %H:%M')
        return f"Venda #{self.pk} - {data_local}"
    
class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    #usamos PROTECT para eviter que um produto seja deletado se ele já fez parte
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    #Armazena o preço no momento da venda, para o caso do preço do produto mudar
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} na Venda #{self.venda.pk}"