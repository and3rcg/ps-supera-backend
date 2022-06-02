import string
import random


def gerar_id(tamanho):
    # gera um ID de pedido, conforme o campo id_pedido em models.Pedido
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=tamanho))
    return str(id)
