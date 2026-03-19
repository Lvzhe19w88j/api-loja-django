from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Pedido, Produto, Pedido_Tabela, Categoria, Cliente
from .serializers import PedidoSerializer, PedidoTabelaSerializer, CategoriaSerializer, ClienteSerializer, ProdutoSerializer

class PedidoViewSet(ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.total_pedido()
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == "Pago":
            try:
                instance.confirmar_pedido()
            except ValueError as e:
                raise serializers.ValidationError(str(e))

class ProdutoViewSet(ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class PedidoTabelaViewSet(ModelViewSet):
    queryset = Pedido_Tabela.objects.all()
    serializer_class = PedidoTabelaSerializer

class CategoriaViewSet(ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
