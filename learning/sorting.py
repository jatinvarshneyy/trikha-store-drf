from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

# Again we need to import first
from rest_framework.filters import SearchFilter, OrderingFilter

from store.models import Product, OrderItem
from store.serializers import ProductSerializer
from store.filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend

# ProductViewSet
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Adding Imported SearchFilter in filter_backends
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'collection__title']
    
    # This is how we use sorting
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product Cannot be allowed because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)