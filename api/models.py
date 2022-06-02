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
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.get_full_name().title()


class Produto(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False, default='Jogo')
    preco = models.FloatField(blank=False, null=False, default=0)
    score = models.IntegerField(blank=False, null=False, verbose_name='Popularidade')
    slug = models.SlugField(blank=True, null=True)
    estoque = models.PositiveIntegerField(blank=False, null=False, default=1)
    listado = models.BooleanField(blank=False, null=False, default=True)

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # arredondar o preço e criar slug automaticamente
        self.preco = round(self.preco, 2)
        if self.slug is None:
            self.slug = slugify(self.nome)
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
        ('aguardando pagamento', 'Aguardando pagamento'),
        ('carrinho', 'Carrinho'),
    )

    id_pedido = models.CharField(max_length=12, unique=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    frete = models.FloatField()
    subtotal = models.FloatField()
    total = models.FloatField()  # subtotal + frete
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='carrinho')

    def save(self, *args, **kwargs):
        if self.subtotal >= 250:
            self.frete = 0

        self.total = self.subtotal + self.frete
        super().save(*args, **kwargs)


class ItemPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(null=False, blank=False, default=1)
