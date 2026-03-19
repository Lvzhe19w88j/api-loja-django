from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, PedidoTabelaViewSet, CategoriaViewSet, ClienteViewSet, ProdutoViewSet

router = DefaultRouter()

router.register('pedido', PedidoViewSet, basename='pedido')
router.register('pedidotabela', PedidoTabelaViewSet, basename='pedidotabela')
router.register('categoria', CategoriaViewSet, basename='categoria')
router.register('cliente', ClienteViewSet, basename='cliente')
router.register('produto', ProdutoViewSet, basename='produto')

urlpatterns = router.urls
