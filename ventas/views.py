from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from ventas.models import *
from ventas.serializers import *


class Pagination(PageNumberPagination):
    page_size = 10  # Cantidad de clientes por página
    page_size_query_param = "page_size"  # Permite cambiar la cantidad con ?page_size=20
    max_page_size = 100  # Límite máximo por página


class VentaCabeceraViewSet(viewsets.ModelViewSet):
    queryset = VentaCabecera.objects.all()
    serializer_class = VentaCabeceraSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    pagination_class = Pagination  # Activa la paginación
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["codigo", "nombre"]  # Filtros exactos (?codigo=123)
    search_fields = ["codigo", "nombre"]  # Búsqueda con "search" (?search=Juan)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    pagination_class = Pagination  # Activa la paginación
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["codigo", "nombre"]  # Filtros exactos (?codigo=123)
    search_fields = ["codigo", "nombre", "direccion"]  # Búsqueda con "search" (?search=Juan)


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer


class VendedorViewSet(viewsets.ModelViewSet):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
