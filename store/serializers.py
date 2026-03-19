from rest_framework import serializers
from .models import Pedido, Pedido_Tabela, Produto, Cliente, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'nome',
            'descricao'
        ]

class ProdutoSerializer(serializers.ModelSerializer):
    categoria = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all()
    )
    
    class Meta:
        model = Produto
        fields = [
            'nome',
            'descricao',
            'preco',
            'estoque',
            'ativo',
            'status',
            'categoria'
                  ]

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'user',
            'telefone', 
            'cpf', 
            'endereco'
            ]

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = [
            'cliente',
            'status',
            'valor_total'
            ]

class PedidoTabelaSerializer(serializers.ModelSerializer):
    
    produto = serializers.PrimaryKeyRelatedField(
        queryset = Produto.objects.all()
    )
    
    pedido = serializers.PrimaryKeyRelatedField(
        queryset = Pedido.objects.all()
    )
    
    def validate(self, data):
        produto = data['produto']
        quantidade = data['quantidade']
        if produto.estoque < quantidade:
            raise serializers.ValidationError(f"Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque}")
        if quantidade <= 0:
            raise serializers.ValidationError("Quantidade deve ser positiva.")
        return data
    
    class Meta:
        model = Pedido_Tabela
        fields = [
            'produto',
            'pedido',
            'quantidade',
            'preco_m'
        ]
