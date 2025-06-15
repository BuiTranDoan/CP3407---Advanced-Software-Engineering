from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CustomizationViewSet, MenuItemViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'customizations', CustomizationViewSet)
router.register(r'menu-items', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]