from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Product List : ListCreateAPIView
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
# Product Detail : RetrieveUpdateDestroyAPIView
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    
    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product Cannot be allowed because it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Collection List : ListCreateAPIView
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

# Collection Detail : RetrieveUpdateDestroyAPIView
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    
    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), id=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection Cannot be allowed because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)