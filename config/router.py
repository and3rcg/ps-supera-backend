from api.views import PedidoViewset, ProdutoViewset, EnderecoViewset, ItemPedidoViewset
from rest_framework import routers

api_router = routers.DefaultRouter()

api_router.register('pedidos', PedidoViewset)
api_router.register('produtos', ProdutoViewset)
api_router.register('enderecos', EnderecoViewset)
api_router.register('itens_pedido', ItemPedidoViewset)
