from django.db import models
import uuid 

# Create your models here.
def gerar_codigo_unico():
    #gera um código unico de 8 caracteres
    return uuid.uuid4().hex.upper()[:8]

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    #o codigo será gerado automaticamente e não será editável no admin
    codigo = models.CharField(max_length=8, unique=True, blank=True, editable=False)
    ativo = models.BooleanField(default=True)
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            #gera um código apenas se o produto ainda não tiver um 
            self.codigo = gerar_codigo_unico()
        super().save(*args, **kwargs)