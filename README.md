# Supera Games - Back-end

Projeto relativo ao processo seletivo de Desenvolvedor Python para a empresa Supera Inovação e Tecnologia.  
Esse projeto consiste na criação de um backend e API com Django, banco de dados PostgreSQL e front-end com React (repositório), containerizados com Docker Compose.

# Sumário

1. [Instruções de inicialização](#instruções-de-inicialização)
2. [Endpoints da API](#endpoints-da-api)
3. [Referência da API](#referência-da-api)
4. [Notas adicionais](#notas-adicionais)

## Instruções de inicialização

-   Clonar este repositório (`git clone`);
-   Criar e ativar um ambiente virtual Python (`python -m venv venv && source venv/bin/activate` no Linux);
-   Instalar as dependências (`pip install -r requirements.txt`);
-   Iniciar a aplicação Docker (`docker-compose up`);
-   Executar as migrações (`docker exec supera_backend python manage.py migrate`);
-   Pré-popular o banco de dados com os jogos do arquivo `products.json` fornecido, com o comando `docker exec supera_backend python manage.py preencherdb`;
-   Inicializar o [front-end](https://github.com/and3rcg/ps-supera-frontend)

## Endpoints da API

Todos os endpoints abaixo foram montados com variações do `ModelViewset` fornecido pelo Django REST Framework, e eles vêm da mesma URL base: `127.0.0.1:8000/api/`

-   `produtos/` (GET): visualização dos produtos disponíveis para venda. É possível colocar um query param na URL no formato `?ordem=<campo_desejado>` para ordenar por `nome`, `score` ou `preco`;
    -   `produtos/<id>/adicionar_ao_carrinho/` (POST): Adiciona um produto ao carrinho.
-   `enderecos/` (GET, POST, PATCH, DELETE): Apenas usuários autenticados podem acessar os dados do endpoint, que irá retornar apenas os endereços registrados pelo usuário.
-   `pedidos/` (GET, POST, PATCH, DELETE): Apenas usuários autenticados podem acessar os pedidos, e o endpoint só retornará os pedidos feitos pelo usuário;
    -   `pedidos/<id>/ver_itens/` (GET): Nesse endpoint é possível verificar os itens comprados num pedido específico;
    -   `pedidos/checkout/` (POST): Nesse endpoint, é concluído o pagamento de algum carrinho
-   `itens_pedido/` (GET, POST, PATCH, DELETE): Aqui, apenas usuários autenticados

## Referência da API

1. Usuários:  
   1.1. Criar usuário: POST em `/api/auth/users`

```json
Body params:
    {
        "username": string,
        "password": string,
        "re_password": string,  // validação de senha, deve ser igual ao password
        "email": string,
        "first_name": string,
        "first_name": string,
        "cpf": string,
    }

Response:
    {
        "data": {
            "username": string,
            "first_name": string,
            "last_name": string,
            "cpf": string,
            "email": string,
            "id": int
        },
        "status": HTTP 201 Created
    }
```

1.2. Login: POST em `/api/auth/jwt/create`

```json
Body params:
    {
        "email": string,
        "password": string
    }

Response:
    {
        "data":
        {
            "access": string,
            "refresh": string
        },
        "status": HTTP 200 OK
    }
```

2. Produtos:  
   2.1. Adicionar um produto ao carrinho: POST em `/api/produtos/<id:int>/adicionar_ao_carrinho/`

```json
Headers:
    {
        "Content-type": "application/json",
        "Authorization": "JWT <access_token>"
    }

Body params:
    {
        "quantidade": int
    }

Response:
    {
        "data": {
            "id": int,
            "id_pedido": string,
            "quantidade": string,
            "frete": float,
            "subtotal": float,
            "total": float,
            "status": string,
            "data_pedido": datetime,
            "cliente": string,
            "endereco": null
        },
        "status": HTTP 201 Created
    }
```

3. Adicionar um endereço: POST em `/api/enderecos/`

```json
Headers:
    {
        "Content-type": "application/json",
        "Authorization": "JWT <access_token>"
    }

Body params:
    {
        "nome": string,
        "cep": string,
        "rua": string,
        "residencia": string,
        "complemento"?: string,
        "bairro": string,
        "cidade": string,
        "estado": string
    }

Response:
    "data": {
        "id": int,
        "nome": string,
        "cep": string,
        "rua": string,
        "residencia": string,
        "complemento": string,
        "bairro": string,
        "cidade": string,
        "estado": string,
        "cliente": int
    },
    "status": HTTP 201 Created
```

4. Checkout de pedido: POST em `/api/pedidos/checkout/`

```json
Headers:
    {
        "Content-type": "application/json",
        "Authorization": "JWT <access_token>"
    }

Body params:
    {
        "endereco": int,
    }

Response:
    "data": {
        "mensagem": "Transação concluída"
    },
    "status": HTTP 200 OK
```

## Notas adicionais:

-   Como esse projeto é apenas um teste prático, uma questão importante de segurança foi desconsiderada: a `SECRET_KEY` do `config/settings.py` está facilmente acessível. Na prática, é recomendado que esse e outros valores mais sensíveis fiquem em um arquivo `.env` na pasta raiz do repositório, e que o mesmo seja ignorado pelo controle de versão, encorajando assim que outros desenvolvedores que queiram executar o projeto localmente criem sua `SECRET_KEY` com auxílio externo e adicionem-a nesse arquivo.
