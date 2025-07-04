from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name = "app"),
    path('sobre-nos', views.sobreNos, name="sobreNos"),
    path('dashboard', views.dashboard , name = "dashboard"),
    path('login', views.login , name = "login"),
    path('usuarios', views.exibirUsuarios, name = "exibirUsuarios"),
    path('add-usuario', views.addUsuario, name="addUsuario"),
    path('excluir-usuario/<int:id_usuario>', views.excluirUsuario, name="excluirUsuario" ),
    path('editar-usuario/<int:id_usuario>', views.editarUsuario, name="editarUsuario"),

    path('cadastrar-produto', views.cadastrarProduto, name="cadastrarProduto" ),
    path('cards-produtos', views.cardsProdutos, name="cardsProdutos"),
    path('listar-produtos', views.listarProdutos, name="listarProdutos" ),
    path('excluir-produto/<int:id_produto>', views.excluirProduto, name="excluirProduto" ),
    path('editar-produto/<int:id_produto>', views.editarProduto, name="editarProduto" ),
    path('grafico-vendas', views.grafico_vendas, name="graficoVendas" ),
    path('grafico', views.grafico, name="grafico"),
    path('categorias', views.getCategorias, name="categorias"),
    path('categoria/<int:id_categoria>/', views.getCategoriaID, name="categoriaID"),
    path('checkout/<int:produto_id>/', views.checkout, name='checkout'),
    path('compras', views.compras, name="compras" ),
    path('logout', views.logout , name = "logout"),

]