from django.db import models
from produtos.models import Produto

# Create your models here.
class Estoque(models.Model):
    #cria uma relação 'um-pra-um' com o produto
    #cada produto terá apenas um registro de estoque
    #on_delete = models.cascade: se o produto for deletado, seu estoque tambem será 
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=10, verbose_name="Estoque Minimo")

    def __str__(self):
        return f"Estoque de {self.produto.nome}"
    
    class Meta:
        verbose_name = "Controle de Estoque"
        verbose_name_plural = "Controles de Estoque"