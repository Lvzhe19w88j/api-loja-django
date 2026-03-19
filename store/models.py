from django.db import models
from django.db.models import Sum, F, Min
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.validators import RegexValidator
from typing import TYPE_CHECKING
from django.db import transaction

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(max_length=150)
    
    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    
    CHOICES_STATUS = (
        ("disponivel", "este produto esta disponivel"),
        ("indisponivel", "este produto nao esta disponivel"),
    )
    
    nome = models.CharField(max_length=50)
    descricao = models.TextField(max_length=150)
    preco = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal(0.1))
        ]        
        )
    
    estoque = models.IntegerField(
        default=0, 
        validators=[
            MinValueValidator(1)
        ]
        )
    
    ativo = models.BooleanField(default=True)
    at_date  = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=CHOICES_STATUS)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=100)
    cpf_validador = RegexValidator(
        regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
    )
    cpf = models.CharField(max_length=14)
    endereco = models.CharField(
        max_length=150,
        validators=[cpf_validador],
        
    )
    
    def __str__(self):
        return self.user

class Pedido(models.Model):
    
    CHOICES_STATUS = (
        ("Pago", "o pedido foi pago!"),
        ("Enviado", "o pedido foi enviado"),
        ("Cancelado", "o pedido foi cancelado"),
    
    )
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_pedido = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=18, choices=CHOICES_STATUS)
    valor_total = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        default=Decimal("0.0"),
        )
    estoque = models.IntegerField(default=0)
    
    if TYPE_CHECKING:
        itens: models.QuerySet["Pedido_Tabela"]
    
    def total_pedido(self):
        total = self.itens.aggregate(
            total=Sum(F("quantidade") * F("preco_m"))
        )["total"] or 0

        self.valor_total = total
        self.save()
    
    @transaction.atomic
    def confirmar_pedido(self):
        if self.status != "Pago":
            raise ValueError("Pedido deve estar pago para confirmar.")
        
        # Validar e subtrair estoque
        for item in self.itens.all():
            if item.produto.estoque < item.quantidade:
                raise ValueError(f"Estoque insuficiente para {item.produto.nome}")
            item.produto.estoque -= item.quantidade
            item.produto.save()
        
        # Calcular total
        self.total_pedido()
        self.save()
        return True
       
class Pedido_Tabela(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)
    preco_m = models.DecimalField(decimal_places=2, max_digits=20)
    
    def clean(self):
        if not self.produto.ativo:
            raise Exception("Produto inativo não pode ser comprado.")
        
        #nao esquecer de fazer anotação de tudo que modificou
        