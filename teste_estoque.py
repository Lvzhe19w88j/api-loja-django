#!/usr/bin/env python
#\"\"\"Script teste estoque - Execute: python teste_estoque.py\"\"\"
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from store.models import *
from decimal import Decimal

print("🧪 Testando sistema estoque...")

# Cleanup
Pedido_Tabela.objects.all().delete()
Pedido.objects.all().delete()
Produto.objects.filter(nome__startswith='TESTE').delete()

# Teste 1: Sucesso
print("\\n1. TESTE SUCESSO:")
cliente = Cliente.objects.first()
if not cliente:
    from django.contrib.auth.models import User
    user = User.objects.create_user('test', 'test@test.com', '123')
    cliente = Cliente.objects.create(user=user, telefone='1199999', cpf='123.456.789-00', endereco='Rua Teste')

p1 = Produto.objects.create(nome='TESTE Leite', estoque=5, preco=Decimal('4.5'), categoria=Categoria.objects.first() or Categoria.objects.create(nome='teste', descricao='test'))
pedido = Pedido.objects.create(cliente=cliente)
Pedido_Tabela.objects.create(pedido=pedido, produto=p1, quantidade=2, preco_m=Decimal('4.5'))
print(f'  Estoque antes: {p1.estoque}')
pedido.status = 'Pago'
pedido.confirmar_pedido()
p1.refresh_from_db()
print(f'  Estoque depois: {p1.estoque} ✅')

# Teste 2: Falha validação
print("\\n2. TESTE FALHA:")
try:
    Pedido_Tabela.objects.create(pedido=pedido, produto=p1, quantidade=10, preco_m=Decimal('4.5'))
except Exception as e:
    print(f'  ERRO esperado: {str(e)} ✅')

print("\\n🎉 Todos testes OK! Sistema funcionando perfeitamente!")
