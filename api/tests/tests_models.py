from django.test import TestCase

from ..models import Endereco, Pedido, Produto, User
from ..utils import gerar_id


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username='joaobobo123',
            email='jbobo123@yopmail.com',
            first_name='joão',
            last_name='bobo',
            cpf='11122233344',
            password='foo'
        )

        User.objects.create(
            username='adminbolado',
            email='admbolado123@yopmail.com',
            first_name='admin',
            last_name='bolado',
            password='bar',
            is_superuser=True
        )

    def test_user_str(self):
        user_normal = User.objects.get(email='jbobo123@yopmail.com')
        self.assertEqual(user_normal.__str__(), 'João Bobo')

    def test_superuser(self):
        super_user = User.objects.get(email='admbolado123@yopmail.com')
        self.assertTrue(super_user.is_superuser)


class ProdutoTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Produto.objects.create(  # slug automático
            nome='Super Mario Odyssey',
            preco=197.875,
            score=100,
        )

        Produto.objects.create(  # jogo com slug personalizado
            nome='Call Of Duty Infinite Warfare',
            preco=49.99,
            score=80,
            slug='cod-iw-ps4',
        )

    def test_slug_produto(self):
        p1 = Produto.objects.get(nome='Super Mario Odyssey')
        p2 = Produto.objects.get(nome='Call Of Duty Infinite Warfare')

        self.assertEqual(p1.slug, 'super-mario-odyssey')
        self.assertEqual(p2.slug, 'cod-iw-ps4')

    def test_preco_round(self):
        p1 = Produto.objects.get(nome='Super Mario Odyssey')

        self.assertEqual(p1.preco, 197.88)


class PedidoTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        joao_bobo = User.objects.create(
            username='joaobobo123',
            email='jbobo123@yopmail.com',
            first_name='joão',
            last_name='bobo',
            password='foo'
        )

        # pedido de três produtos com subtotal de 197.88: o total deve ser 227.88
        Pedido.objects.create(
            subtotal=197.88,
            id_pedido=gerar_id(12),
            cliente=joao_bobo,
            quantidade=3
        )

        # pedido de cinco produtos com subtotal de 250: o total deve ser 250
        Pedido.objects.create(
            id_pedido=gerar_id(12),
            subtotal=250,
            cliente=joao_bobo,
            quantidade=5
        )

    def test_total(self):
        p1 = Pedido.objects.get(subtotal=197.88)
        p2 = Pedido.objects.get(subtotal=250)

        self.assertEqual(p1.total, 227.88)
        self.assertEqual(p2.total, 250)


class EnderecoTestCase(TestCase):  # ok
    @classmethod
    def setUpTestData(cls):
        joao_bobo = User.objects.create(
            username='joaobobo123',
            email='jbobo123@yopmail.com',
            first_name='joão',
            last_name='bobo',
            password='foo'
        )

        Endereco.objects.create(
            cliente=joao_bobo,
            nome=joao_bobo.get_full_name(),
            cep='11111111',
            rua='Rua dos Bobos',
            residencia='0',
            bairro='Fictício',
            cidade='Bobolândia',
            estado='Fictício',
        )

    def test_endereco(self):
        e1 = Endereco.objects.get(rua='Rua dos Bobos')

        self.assertEqual(e1.nome, 'joão bobo')
