from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from app.models import Usuario, Produto, Categoria
from app.forms import formUsuario, formProduto, formLogin

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
            formUser.save()
            return redirect("exibirUsuarios")
    return render(request, "add-usuario.html", {'form':formUser})

def excluirUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.delete()
    return redirect("exibirUsuarios")

def editarUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    formUser = formUsuario(request.POST or None, instance=usuario)
    if request.POST:
        if formUser.is_valid():
            formUser.save()
            return redirect("exibirUsuarios")
    return render(request, "editar-usuario.html", {'form': formUser})

def login(request):
    frmLogin = formLogin(request.POST or None)
    if request.POST:
        if frmLogin.is_valid():
            _email = frmLogin.cleaned_data.get('email')
            _senha = frmLogin.cleaned_data.get('senha')
            try:
                userLogin = Usuario.objects.get(email=_email,senha= _senha)
                if userLogin is not None:
                    request.session.set_expiry(timedelta(seconds=600))
                   
                    request.session['email'] = _email
                    tempo_sessao = timedelta(seconds=600)
                    tempo_sessao_segundos = tempo_sessao.total_seconds()
                    request.session['tempo_sessao_segundos '] =  tempo_sessao_segundos
                    return redirect("app")
            except Usuario.DoesNotExist:
                return render(request, "login.html")
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
    formProd = formProduto(request.POST or None, instance=produto)

    if request.POST:
        if formProd.is_valid():
            formProd.save()
            return redirect("listarProdutos")
        
    return render(request, "editar-produto.html", {'form': formProd})

def cardsProdutos(request):
    produtosapi = requests.get("https://fakestoreapi.com/products").json()
    return render(request,"listar-produtos.html",{'produtos':produtosapi})

def grafico(request):
    produtos = Produto.objects.all()
    nome = [produto.nome for produto in produtos]
    estoque = [produto.estoque for produto in produtos]

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
    