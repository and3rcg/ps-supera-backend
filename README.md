# Supera Games - Backend

Projeto relativo ao processo seletivo de Desenvolvedor Python para a empresa Supera Inovação e Tecnologia.  
Esse projeto consiste na criação de um backend e API com Django, banco de dados PostgreSQL e front-end com React (repositório), containerizados com Docker Compose.

# Sumário

1. [Instruções de inicialização](#instruções-de-inicialização)
2. [Endpoints da API](#endpoints-da-api)
3. [Notas adicionais](#notas-adicionais)

## Instruções de inicialização

-   Clonar este repositório (`git clone`);
-   Criar e ativar um ambiente virtual Python (`python -m venv venv && source venv/bin/activate` no Linux);
-   Instalar as dependências (`pip install -r requirements.txt`);
-   Iniciar a aplicação Docker (`docker-compose up`).

-   Executar as migrações (`docker exec supera-backend python manage.py migrate`)

## Endpoints da API

Todos os endpoints abaixo foram montados com variações do `ModelViewset` fornecido pelo Django REST Framework, e eles vêm da mesma URL base: `127.0.0.1:8000/api/`

-   `produtos/` (GET): visualização dos produtos disponíveis para venda. É possível colocar um query param na URL no formato `?ordem=<campo_desejado>` para ordenar por `nome`, `score` ou `preco`;
    -   `produtos/<id>/adicionar_ao_carrinho/` (POST): Adiciona um produto ao carrinho.
-   `enderecos/` (GET, POST, PATCH, DELETE): Apenas usuários autenticados podem acessar os dados do endpoint, que irá retornar apenas os endereços registrados pelo usuário.
-   `pedidos/` (GET, POST, PATCH, DELETE): Apenas usuários autenticados podem acessar os pedidos, e o endpoint só retornará os pedidos feitos pelo usuário;
    -   `pedidos/<id>/ver_itens/` (GET): Nesse endpoint é possível verificar os itens comprados num pedido específico;
    -   `pedidos/checkout/` (POST): Nesse endpoint, é concluído o pagamento de algum carrinho
-   `itens_pedido/` (GET, POST, PATCH, DELETE): Aqui, apenas usuários autenticados

## Notas adicionais:

-   Como esse projeto é apenas um teste prático, uma questão importante de segurança foi desconsiderada: a `SECRET_KEY` do `config/settings.py` está facilmente acessível. Na prática, é recomendado que esse e outros valores mais sensíveis fiquem em um arquivo `.env` na pasta raiz do repositório, e que o mesmo seja ignorado pelo controle de versão, encorajando assim que outros desenvolvedores que queiram executar o projeto localmente criem sua `SECRET_KEY` com auxílio externo e adicionem-a nesse arquivo.
