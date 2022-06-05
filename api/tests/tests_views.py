from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Endereco, ItemPedido, Pedido, Produto, User
from ..utils import gerar_id


class UsuarioTestCase(APITestCase):
    """
        testar os endpoints fornecidos por ProdutoViewset
    """

    def test_registro_login(self):
        # testar o registro e o login de um usuário novo
        data_registro = {'username': 'testcase',
                         'email': 'testcase@yopmail.com',
                         'password': 'some_strong_password123',
                         're_password': 'some_strong_password123',
                         'first_name': 'test',
                         'last_name': 'case',
                         'cpf': '12233344445',
                         }

        data_login = {
            'email': 'testcase@yopmail.com',
            'password': 'some_strong_password123'
        }

        response = self.client.post("/api/auth/users/", data_registro)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # login
        response = self.client.post("/api/auth/jwt/create/", data_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
