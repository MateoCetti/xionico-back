from rest_framework.routers import DefaultRouter
from django.urls import path, include

from ventas.views import *

router = DefaultRouter()
router.register(r'ventas', VentaCabeceraViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'empresas', EmpresaViewSet)
router.register(r'vendedores', VendedorViewSet)

urlpatterns = router.urls
