from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

from .utils import gerar_id


class User(AbstractUser):
    # atualizar o modelo padrão de usuário
    email = models.EmailField(unique=True)
    saldo = models.FloatField(blank=False, null=False, default=0)
    cpf = models.CharField(max_length=11, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'cpf']

    def __str__(self):
        return self.get_full_name().title()


class Produto(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False, default='Jogo')
    preco = models.FloatField(blank=False, null=False, default=0)
    score = models.IntegerField(blank=False, null=False, verbose_name='Popularidade')
    slug = models.SlugField(blank=True, null=True)
    estoque = models.PositiveIntegerField(blank=False, null=False, default=1)
    listado = models.BooleanField(blank=False, null=False, default=True)
    data_adicionado = models.DateTimeField(null=True, auto_now_add=True)
    imagem = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # arredondar o preço, criar slug automaticamente e ocultar produtos fora de estoque
        self.preco = round(self.preco, 2)
        if self.slug is None:
            self.slug = slugify(self.nome)

        if self.estoque == 0:
            self.listado = False
        super().save(*args, **kwargs)


class Endereco(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    rua = models.CharField(max_length=50)
    residencia = models.CharField(max_length=10)
    complemento = models.CharField(max_length=20)
    bairro = models.CharField(max_length=20)
    cidade = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)


class Pedido(models.Model):
    STATUS_CHOICES = (
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
        ('aprovado', 'Pagamento aprovado'),
        ('carrinho', 'Carrinho'),
    )

    id_pedido = models.CharField(max_length=12, blank=True, unique=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    quantidade = models.IntegerField(default=0)  # quantidade total de itens
    frete = models.FloatField(default=0)
    subtotal = models.FloatField(default=0)
    total = models.FloatField(default=0)  # subtotal + frete
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='carrinho')
    data_pedido = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        self.frete = 10 * self.quantidade
        if self.subtotal >= 250:
            self.frete = 0

        if self.id_pedido == "":
            self.id_pedido = gerar_id(12)

        self.total = self.subtotal + self.frete
        super().save(*args, **kwargs)


class ItemPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(null=False, blank=False, default=1)
