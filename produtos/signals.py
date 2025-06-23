from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Produto
from estoque.models import Estoque

@receiver(post_save, sender=Produto)
def criar_estoque_para_novo_produto(sender, instance, created, **kwargs):
    """
    Cria um registro de estoque para cada novo produto criado.
    """

    if created:
        Estoque.objects.create(produto=instance)