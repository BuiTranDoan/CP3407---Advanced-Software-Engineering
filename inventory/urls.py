from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, InventoryItemViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('inventory-items', InventoryItemViewSet, basename='inventoryitem')

urlpatterns = router.urls