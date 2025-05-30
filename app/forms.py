from django import forms
from app.models import Usuario, Produto

class formUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'senha')

        widgets = {
            'nome' : forms.TextInput(attrs={'type':'text'}),
            'email' : forms.TextInput(attrs={'type':'email'}),
            'senha' : forms.TextInput(attrs={'type':'password'}),
        }

class formLogin(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'senha')
        
        widgets = {
            'email': forms.TextInput(attrs={'class':'form-control mb-3' , 'placeholder': 'email'}),
            'senha': forms.TextInput(attrs={'class': 'form-control mb-3', 'type': 'password', 'placeholder': 'senha'}),
        }

class formProduto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ('nomeProduto', 'descricaoProduto', 'precoProduto', 'imagemProduto', 'qtdeEstoque', 'categoriaProduto')

        widgets = {
            'nomeProduto' : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'nome do produto'}),
            'descricaoProduto': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'descrição' }),
            'precoProduto': forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Preço'}),
            'imagemProduto': forms.FileInput(attrs={'class': 'form-control mb-3', 'placeholder': 'descrição' }),
            'qtdeEstoque': forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Produto em estoque' }),
            'categoriaProduto': forms.Select(attrs={'placeholder': 'Selecione uma categoria'}),
        }