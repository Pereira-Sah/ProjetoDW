from django.db import models
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=100)
    CEP = models.CharField(max_length=9, default='00000-000')
    logradouro = models.CharField(max_length=100, default='Não informado')
    bairro = models.CharField(max_length=100, default='Não informado')
    localidade = models.CharField(max_length=100, default='Não informado')
    estado = models.CharField(max_length=2, default='XX')
    numero_residencia = models.CharField(max_length=10, default='0')

class Login(models.Model):
    usuario = models.CharField(max_length=255)
    email = models.EmailField()
    senha = models.CharField(max_length=16)

class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome}"

class Produto(models.Model):
    nomeProduto = models.CharField(max_length = 200)
    descricaoProduto = models.TextField()
    precoProduto = models.DecimalField(max_digits=10, decimal_places=2)
    imagemProduto = models.ImageField(upload_to='imagens/')
    qtdeEstoque = models.IntegerField()
    categoriaProduto = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)