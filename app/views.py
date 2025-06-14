from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from app.models import Usuario, Produto, Categoria, Venda
from app.forms import formUsuario, formProduto, formLogin, formCheckout
from django.contrib.auth.hashers import make_password, check_password
import requests
import io, urllib, base64
import matplotlib.pyplot as plt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategoriaSerializer

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

def sobreNos(request):
    template = loader.get_template("sobre-nos.html")
    return HttpResponse(template.render())

def exibirUsuarios(request):
    usuarios = Usuario.objects.all().values()
    return render(request, "usuarios.html", {'listUsuarios': usuarios})

        
def addUsuario(request):
    formUser = formUsuario(request.POST or None)        
    if request.POST:

        if formUser.is_valid():
            email = formUser.cleaned_data.get('email')
            senha = formUser.cleaned_data.get('senha')
            confirmar_senha = request.POST.get('confirmar_senha') 
            
            if Usuario.objects.filter(email=email).exists():
                messages.error(request, 'Email já cadastrado. Por favor, use outro email.')
                return render(request, "add-usuario.html", {'form': formUser})
            elif senha != confirmar_senha:
                messages.error(request, 'As senhas não coincidem. Por favor, tente novamente.')
                return render(request, "add-usuario.html", {'form': formUser})
            else:
                usuario = formUser.save(commit=False) 

                usuario.save()                      
                messages.success(request, 'Usuário cadastrado com sucesso!')

                return redirect("login")
        else:
            messages.error(request, 'Erro ao cadastrar usuário. Verifique os dados e tente novamente.')
    
    return render(request, "add-usuario.html", {'form':formUser})

def excluirUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.delete()
    return redirect("exibirUsuarios")

def editarUsuario(request, id_usuario):
    if not request.session.get("email"):
        messages.warning(request, 'Você precisa fazer login para editar usuário.')
        return redirect("login")
    
    usuario = Usuario.objects.get(id=id_usuario)
    email_antigo = usuario.email

    if request.method == "POST":
        formUser = formUsuario(request.POST, instance=usuario)
        if formUser.is_valid():
            senha = formUser.cleaned_data.get('senha')
            confirmar_senha = request.POST.get('confirmar_senha')

            if senha and confirmar_senha and senha != confirmar_senha:
                messages.error(request, 'As senhas não coincidem. Por favor, tente novamente.')
                return render(request, "editar-usuario.html", {'form': formUser})

            usuario = formUser.save(commit=False)
            if senha: 
                usuario.senha = make_password(senha)

            if request.session.get("email") == email_antigo and usuario.email != email_antigo:
                request.session['email'] = usuario.email
                messages.info(request, 'Seu e-mail foi atualizado na sessão.')

            usuario.save()
            messages.success(request, f'Usuário {usuario.nome} editado com sucesso!')
            return redirect("exibirUsuarios")
        else:
            messages.error(request, 'Erro ao editar usuário. Verifique os dados e tente novamente.')
    else:
       
        formUser = formUsuario(instance=usuario)
        formUser.fields['senha'].initial = ''
        formUser.fields['confirmar_senha'].initial = ''

    return render(request, "editar-usuario.html", {'form': formUser})

def login(request):
    frmLogin = formLogin(request.POST or None)
    if request.POST:
        if frmLogin.is_valid():
            _email = frmLogin.cleaned_data.get('email')
            _senha = frmLogin.cleaned_data.get('senha')

            try:
                userLogin = Usuario.objects.get(email=_email)
                if (_senha, userLogin.senha):
                    request.session.set_expiry(timedelta(seconds=600))
                    request.session['email'] = _email

                    tempo_sessao = timedelta(seconds=600)
                    tempo_sessao_segundos = tempo_sessao.total_seconds()

                    request.session['tempo_sessao_segundos'] = tempo_sessao_segundos
                    messages.success(request, 'Login efetuado com sucesso!')
                    return redirect("dashboard")
                
                else:
                    messages.error(request, 'Email ou senha inválidos.')
                    return render(request, "login.html", {'form': frmLogin})
                
            except Usuario.DoesNotExist:
                messages.error(request, 'Email ou senha inválidos.')
                return render(request, "login.html", {'form': frmLogin})
    return render(request, "login.html", {'form': frmLogin})

def cadastrarProduto(request):
    if request.method == 'POST':
        formProduct = formProduto(request.POST, request.FILES)
        if formProduct.is_valid():
            formProduct.save()
            return redirect("listarProdutos")
    return render(request, "cadastrar-produto.html", {'form':formProduto})

def listarProdutos(request):
    produtos = Produto.objects.all().values()
    return render(request, "listar-produtos.html", {'listarProdutos': produtos})

def excluirProduto(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    produto.delete()
    return redirect("listarProdutos")

def editarProduto(request, id_produto):
    produto = Produto.objects.get(id=id_produto)
    formProd = formProduto(request.POST or None, request.FILES or None,instance=produto)

    if request.POST:
        if formProd.is_valid():
            formProd.save()
            return redirect("listarProdutos")
        
    return render(request, "editar-produto.html", {'form': formProd})

def cardsProdutos(request):
    listProdutos = requests.get("https://fakestoreapi.com/products").json()
    produtos = Produto.objects.all()
    return render(request, "cards-produtos.html", {'produtos': listProdutos, 'prods': produtos})
    

def dashboard(request):
    _email = request.session.get("email")
    tempo_sessao = request.session.get("tempo_sessao_segundos")
    if _email is None:
            messages.warning(request, 'Você precisa fazer login para acessar o dashboard.')
            return render(request, "index.html")
    if tempo_sessao and tempo_sessao > 600:
        messages.warning(request, 'Sua sessão expirou. Por favor, faça login novamente.')
        return render(request, "index.html")
    else:
        return render(request, "dashboard.html", {'email' : _email})

def grafico(request):
    produtos = Produto.objects.all()
    nome = [produto.nomeProduto for produto in produtos]
    estoque = [produto.qtdeEstoque for produto in produtos]

    fig, ax = plt.subplots()
    ax.bar(nome, estoque)
    ax.set_xlabel("Produto")
    ax.set_ylabel("Estoque")
    ax.set_title("Produtos")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return render (request, 'grafico.html', {'dados':uri})


def grafico_vendas(request):
    if not request.session.get("email"):
        messages.warning(request, 'Você precisa fazer login para acessar os gráficos.')
        return redirect("login")

    vendas = Venda.objects.all()
    vendas_por_data = {}

    for venda in vendas:
        data_str = venda.data_compra.strftime("%Y-%m-%d")  
        vendas_por_data[data_str] = vendas_por_data.get(data_str, 0) + float(venda.preco_venda)

    datas = list(vendas_por_data.keys())
    totais = list(vendas_por_data.values())

    fig, ax = plt.subplots()
    ax.plot(datas, totais, marker='o', linestyle='-',  color='pink')
    ax.set_title("Total de Vendas por Dia")
    ax.set_xlabel("Data")
    ax.set_ylabel("Total R$")
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return render(request, 'grafico-vendas.html', {'dados': uri})



@api_view(['GET','POST'])
def getCategorias(request):

    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def getCategoriaID(request, id_categoria):
    try:
        categoria = Categoria.objects.get(id=id_categoria)
    except Categoria.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def checkout(request, produto_id):
    if not request.session.get("email"):
        return redirect("login")

    produto = Produto.objects.get(id=produto_id)
    cliente = Usuario.objects.get(email=request.session.get("email"))

    if request.method == 'POST':
        form = formCheckout(request.POST)

        if form.is_valid():
            venda = Venda(
                cliente=cliente,
                produto=produto,
                preco_venda=produto.precoProduto,
                numero_cartao=form.cleaned_data.get('numero_cartao'),
                validade=form.cleaned_data.get('validade'),
                cvv=form.cleaned_data.get('cvv'),
            )
            venda.save()
            messages.success(request, 'Compra realizada com sucesso!')
            # Atualiza o estoque do produto 
            produto.qtdeEstoque -= 1
            produto.save()
            return redirect("compras")
        else:
            messages.error(request, 'Erro ao processar o pagamento. Verifique os dados e tente novamente.')
            return render(request, "checkout.html", {
                "produto": produto,
                "cliente": cliente,
                "form": form
            })
    else:
        form = formCheckout()

    return render(request, "checkout.html", {
        "produto": produto,
        "cliente": cliente,
        "form": form
    })


def compras(request):
    if not request.session.get("email"):
        messages.warning(request, 'Você precisa fazer login para acessar suas compras.')
        return redirect("login")
     
    cliente = Usuario.objects.get(email=request.session.get("email"))
    compras = Venda.objects.filter(cliente=cliente).select_related('produto')

    return render(request, "compras.html", {
        "compras": compras
    })

def logout(request):
    if not request.session.get("email"):
        messages.warning(request, 'Você precisa fazer login para fazer logout.')
        return redirect("login")
    request.session.flush()
    messages.info(request, "Logout realizado com sucesso.")
    return redirect("login")
