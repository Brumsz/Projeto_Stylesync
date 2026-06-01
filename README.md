# StyleSync API

API REST desenvolvida com Flask e MongoDB para gerenciamento de produtos, categorias, usuários e importação de vendas via CSV.

## Tecnologias

- **Python** com **Flask** — framework web
- **MongoDB** com **PyMongo** — banco de dados
- **Pydantic** — validação de dados
- **JWT** — autenticação via token
- **Pytest** — testes automatizados

## Estrutura do Projeto

```
├── app/
│   ├── models/
│   │   ├── category.py     # Modelo de categoria
│   │   ├── product.py      # Modelo de produto
│   │   ├── sales.py        # Modelo de venda
│   │   └── user.py         # Modelo de usuário
│   ├── routes/
│   │   ├── main.py         # Rotas de produtos, login e upload
│   │   ├── category_routes.py  # Rotas de categorias
│   │   └── user_routes.py  # Rotas de usuários
│   ├── decorators.py       # Middleware de autenticação JWT
│   ├── utils.py            # Funções utilitárias
│   └── __init__.py         # Configuração do app e conexão com MongoDB
├── tests/
│   ├── __init__.py
│   └── test_utils.py       # Testes da função format_currency
├── config.py               # Configurações da aplicação
├── run.py                  # Ponto de entrada
└── requirements.txt
```

## Instalação

```bash
# Clone o repositório
git clone https://github.com/Brumsz/Projeto_Stylesync
cd Projeto_Stylesync

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
MONGO_URI= URL do seu mongo db
SECRET_KEY=sua-chave-secreta
```

## Executando

```bash
python run.py
```

A API estará disponível em `http://localhost:5000`.

## Autenticação

A API usa JWT. Para acessar rotas protegidas, faça login e inclua o token no header:

```
Authorization: Bearer <token>
```

### Login

```http
POST /login
Content-Type: application/json

{
  "name": "admin",
  "password": "supersecret"
}
```

Resposta:
```json
{
  "access_token": "<jwt_token>"
}
```

## Endpoints

### Produtos

| Método | Rota | Autenticação | Descrição |
|--------|------|:---:|-----------|
| GET | `/products` | ❌ | Lista todos os produtos |
| GET | `/products/:id` | ❌ | Busca produto por ID |
| POST | `/products` | ✅ | Cria novo produto |
| PUT | `/product/:id` | ✅ | Atualiza produto |
| DELETE | `/product/:id` | ✅ | Deleta produto |

**Criar produto:**
```json
{
  "name": "Camiseta",
  "price": 99.90,
  "stock": 10,
  "description": "Camiseta básica"
}
```

### Categorias

| Método | Rota | Autenticação | Descrição |
|--------|------|:---:|-----------|
| GET | `/categorys/all` | ❌ | Lista todas as categorias |
| GET | `/categorys/:id` | ❌ | Busca categoria por ID |
| POST | `/categorys/` | ✅ | Cria nova categoria |
| DELETE | `/categorys/:id` | ✅ | Deleta categoria |

**Criar categoria:**
```json
{
  "name": "Camisetas",
  "description": "Linha de camisetas"
}
```

### Usuários

| Método | Rota | Autenticação | Descrição |
|--------|------|:---:|-----------|
| GET | `/user/all` | ✅ | Lista todos os usuários |
| POST | `/user` | ✅ | Cria novo usuário |
| DELETE | `/user/:id` | ✅ | Deleta usuário |

**Criar usuário:**
```json
{
  "name": "joao",
  "password": "senha123"
}
```

### Upload de Vendas

| Método | Rota | Autenticação | Descrição |
|--------|------|:---:|-----------|
| POST | `/sales/upload` | ✅ | Importa vendas via CSV |

O arquivo CSV deve conter as colunas:

```
sale_date,product_id,quantity,total_value
2024-01-15,507f1f77bcf86cd799439011,5,499.50
```

Resposta:
```json
{
  "message": "Upload processado com sucesso.",
  "vendas_importadas": 12,
  "erros_encontrados": []
}
```

## Testes

```bash
pytest
```

Os testes cobrem a função utilitária `format_currency`, que formata valores monetários no padrão brasileiro.

```
tests/test_utils.py::test_format_currency_with_decimal PASSED
tests/test_utils.py::test_format_currency_with_integer PASSED
tests/test_utils.py::test_format_currency_with_zero    PASSED
```
