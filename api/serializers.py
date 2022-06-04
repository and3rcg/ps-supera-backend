from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from djoser.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Produto, Pedido, ItemPedido, Endereco

User = get_user_model()


class RegistroSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (settings.LOGIN_FIELD,)

    def create(self, validated_data):
        """
        customizing the create method to encrypt the passwords
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class PerfilSerializer(UserSerializer):
    # Customize the data provided by the /users/me/ endpoint:
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'cpf',
        )
        read_only_fields = (settings.LOGIN_FIELD,)


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'


class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'
