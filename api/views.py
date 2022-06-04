from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import Produto, Pedido, ItemPedido, Endereco
from .serializers import *
from .utils import gerar_id


User = get_user_model()


class ProdutoViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Produto.objects.filter(listado=True)
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        # garantir que o queryset será reavaliado em cada solicitação (self.queryset fica em cache)
        queryset = super().get_queryset()

        if self.request.query_params:
            # colocar as ordenações no formato de URL Params (ex: ?ordem=nome)
            query_params = self.request.query_params
            if 'ordem' in query_params:
                campo_ordem = query_params.get('ordem')
                return queryset.order_by(campo_ordem)

        return queryset

    @action(detail=True, methods=['post'])
    def adicionar_ao_carrinho(self, request, pk=None):
        cliente_atual = request.user
        produto_atual = self.get_object()

        pedido_atual, criado = Pedido.objects.get_or_create(
            cliente=cliente_atual,
            status='carrinho',
            defaults={'id_pedido': gerar_id(12)},
        )

        produto_comprado = ItemPedido.objects.create(
            produto=produto_atual,
            pedido=pedido_atual,
            quantidade=int(request.data.get('quantidade'))
        )

        pedido_atual.quantidade += produto_comprado.quantidade
        # dez reais de frete para cada produto no pedido
        pedido_atual.frete = 10 * pedido_atual.quantidade
        pedido_atual.subtotal += produto_atual.preco * produto_comprado.quantidade
        pedido_atual.save()

        pedido_serializer = PedidoSerializer(pedido_atual)

        if criado:
            return Response(data=pedido_serializer.data, status=status.HTTP_201_CREATED)
        # se já foi encontrado um pedido com status 'carrinho' do cliente atual, então:
        return Response(data=pedido_serializer.data, status=status.HTTP_200_OK)


class EnderecoViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Endereco.objects.all()

    def list(self, request):
        cliente = request.user
        queryset = Endereco.objects.filter(cliente=cliente)
        serializer = EnderecoSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PedidoViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Pedido.objects.all()

    def list(self, request):
        cliente = request.user
        queryset = Pedido.objects.filter(cliente=cliente)
        serializer = PedidoSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def ver_itens(self, request, pk=None):
        # endpoint para verificar todos os produtos de um pedido específico
        pedido_atual = self.get_object()
        itens_pedido = ItemPedido.objects.filter(pedido=pedido_atual)
        serializer = ItemPedidoSerializer(itens_pedido, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        '''
        Fazer checkout de um pedido:
            Validar endereço do usuário, verificar saldo e estoque, deduzir saldo
            deduzir estoque dos produtos
        '''
        cliente_atual = request.user
        id_endereco = int(request.data.get('endereco'))
        carrinho = Pedido.objects.get(cliente=cliente_atual, status='carrinho')
        itens_carrinho = ItemPedido.objects.filter(pedido=carrinho)

        # verificações de saldo e endereço do cliente
        endereco = Endereco.objects.get(id=id_endereco)

        if (endereco.cliente != cliente_atual):
            return Response({'erro': 'O endereço enviado não pertence a você.'}, status=status.HTTP_400_BAD_REQUEST)
        elif (cliente_atual.saldo < carrinho.total):
            return Response({'erro': 'Saldo insuficiente.'}, status=status.HTTP_400_BAD_REQUEST)

        # verificação de estoque dos produtos
        for item_comprado in itens_carrinho:
            produto = item_comprado.produto
            if produto.estoque < item_comprado.quantidade:
                return Response({'erro': f'Produto {produto.nome} fora de estoque.'}, status=status.HTTP_400_BAD_REQUEST)

        # dedução dos produtos em estoque
        for item_comprado in itens_carrinho:
            produto = item_comprado.produto
            produto.estoque -= item_comprado.quantidade

            if produto.estoque == 0:  # ocultar o produto do site se ficar fora de estoque
                produto.listado = False
            produto.save()

        # dedução do saldo do cliente
        cliente_atual.saldo -= carrinho.total
        cliente_atual.save()

        # alteração do status do pedido para pagamento aprovado
        carrinho.status = 'aprovado'
        carrinho.save()

        return Response({'mensagem': 'Transação concluída.'}, status=status.HTTP_200_OK)


class ItemPedidoViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ItemPedido.objects.all()

    def destroy(self, request, pk=None):
        # atualizar pedidos ao remover itens do carrinho
        item_atual = self.get_object()
        pedido = item_atual.pedido
        produto = item_atual.produto

        if pedido.status != 'carrinho':
            return Response({'erro': 'Itens de pedidos fechados não podem ser apagados'}, status=status.HTTP_400_BAD_REQUEST)

        # atualizar o status do pedido atual
        pedido.subtotal -= produto.preco * item_atual.quantidade
        pedido.frete = 10 * pedido.quantidade
        pedido.save()

        super().destroy(request, pk)
