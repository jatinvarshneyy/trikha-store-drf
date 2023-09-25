"""
- Very first we need to install django_filters using pip
- Then we need to configure in installed_apps in settings.py

- We need to make an separate file called 'filters.py'
"""

# -----------------> Product Filter : Starts Here <---------------------
from django_filters.rest_framework import FilterSet
from store.models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt']
        }
# -----------------> Product Filter : Ends Here <-----------------------


# ----> How we configure the custom filter in our views function:
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from store.models import Product, OrderItem
from store.serializers import ProductSerializer
from store.filters import ProductFilter

# Import this
from django_filters.rest_framework import DjangoFilterBackend

# ProductViewSet
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Using This
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product Cannot be allowed because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs) 