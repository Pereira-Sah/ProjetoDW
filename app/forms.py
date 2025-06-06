from django import forms
from app.models import Usuario, Produto, Venda

class formUsuario(forms.ModelForm):
    confirmar_senha = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3', 
            'type': 'password', 
            'placeholder': 'confirmar senha'
        })
    )
    class Meta:
        model = Usuario
        fields = ('nome', 'email', 'senha', 'CEP', 'logradouro', 'bairro', 'localidade', 'estado', 'numero_residencia' )
        
        widgets = {
            'nome' : forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Nome'}),
            'email': forms.TextInput(attrs={'class':'form-control mb-3' , 'placeholder': 'Email'}),
            'senha': forms.TextInput(attrs={'class': 'form-control mb-3', 'type': 'password', 'placeholder': 'Senha'}),
            'CEP': forms.TextInput(attrs={'class':'form-control mb-3' , 'placeholder': 'CEP', 'onblur': 'buscaCep(this.value)', 'id': 'cep'}),
            'logradouro': forms.TextInput(attrs={'class':'form-control mb-3' , 'placeholder': 'Logradouro','id': 'logradouro'}),
            'bairro': forms.TextInput(attrs={'class':'form-control mb-3' , 'placeholder': 'Bairro','id': 'bairro'}),
            'localidade': forms.TextInput(attrs={'class':'form-control mb-3' , 'placeholder': 'Localidade','id': 'localidade'}),
            'estado': forms.TextInput(attrs={'class':'form-control mb-3' , 'placeholder': 'Estado','id': 'estado'}),
            'numero_residencia': forms.TextInput(attrs={'class':'form-control mb-3' , 'placeholder': 'Número','id': 'numero'}),
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


class formCheckout(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ('numero_cartao', 'validade', 'cvv')

        widgets = {
            'numero_cartao': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '0000 0000 0000 0000'}),
            'validade': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '12/26'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': '123'}),
        }