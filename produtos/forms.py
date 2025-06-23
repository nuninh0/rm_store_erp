from django import forms
from . models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco'] #apenas os campos que o usuario deve preencher 
        