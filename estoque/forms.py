from django import forms
from .models import Estoque

class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        #apenas os campos que o ususário poderá editarnesta tela
        fields = ['quantidade', 'estoque_minimo']