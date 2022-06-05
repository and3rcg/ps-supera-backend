import json

from api.models import Produto
from django.core.management.base import BaseCommand

# sort cards by latest: first existing card will mean the database is updated.
api_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?sort=new&format=tcg'


class Command(BaseCommand):
    help = 'Preenche o banco de dados com o arquivo products.json fornecido.'

    def handle(self, *args, **options):
        with open('api/management/commands/products.json', 'r') as f:
            data = json.load(f)
            for jogo in data:
                Produto.objects.create(
                    nome=jogo['name'],
                    preco=jogo['price'],
                    score=jogo['score'],
                    imagem=jogo['image'],
                    estoque=50
                )
                print(f"Produto {jogo['name']} adicionado com sucesso!")
