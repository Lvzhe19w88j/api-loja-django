# 🛒 API Loja - Django REST + JWT

API REST para gerenciamento de clientes, pedidos e controle de estoque.

Projeto desenvolvido com foco em boas práticas de backend, segurança e integridade de dados.

---

## 🚀 Tecnologias Utilizadas

- Python 3
- Django
- Django REST Framework
- SimpleJWT (Autenticação JWT)
- SQLite
- typing
- transaction.atomic
- F() expressions
- Sum() aggregation

---

## 🔐 Autenticação com JWT

A autenticação é feita utilizando JSON Web Token (JWT).

### 🔑 Obter Token

POST:


/api/token/


Body:

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}

Resposta:

{
  "access": "token_aqui",
  "refresh": "refresh_token_aqui"
}

🔄 Atualizar Token

POST:

/api/token/refresh/

Body:

{
  "refresh": "refresh_token_aqui"
}
🔐 Usar Token nas Requisições

Header:

Authorization: Bearer seu_token_aqui

🧠 Conceitos Avançados Aplicados

Atualização segura de estoque com F()
Agregações com Sum()
Validações personalizadas
Controle de concorrência com transaction.atomic()
Tipagem com typing
Separação de responsabilidades (models, serializers, views)

⚙️ Funcionalidades

Cadastro de clientes
Controle de estoque
Criação de pedidos
Autenticação segura com JWT
Validação de dados
Controle transacional

▶️ Como rodar o projeto
1️⃣ Clone o repositório
git clone https://github.com/SEUUSUARIO/api-loja-django.git
cd api-loja-django
2️⃣ Crie ambiente virtual
python -m venv venv
venv\Scripts\activate
3️⃣ Instale dependências
pip install -r requirements.txt
4️⃣ Execute migrações
python manage.py migrate
5️⃣ Crie superusuário
python manage.py createsuperuser
6️⃣ Rode o servidor
python manage.py runserver

Servidor disponível em:

http://127.0.0.1:8000/
📂 Estrutura do Projeto
project/      # Configurações do Django
store/        # App principal
manage.py
requirements.txt

Autor
Luiz Victor
---

# 🚀 Depois disso

Salve e rode:

```bash
git add README.md
git commit -m "Improve README with JWT documentation"
git push
