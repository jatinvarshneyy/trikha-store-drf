from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status
from store.models import Product
from store.serializers import ProductSerializer

""" 
----> This method is use when we want override the methods.
"""
# Product List View : ListCreateAPIView
class ProductList(ListCreateAPIView):
    def get_queryset(self):
        return Product.objects.select_related('collection').all()
    
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
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

    """ 
    ----> When we use ListCreateAPIView, we have the option to define individual methods as needed. However, we typically override these methods when customization is required. Otherwise, the Django Rest Framework provides us with default implementations for these methods.In summary, by only overriding the methods that need customization and utilizing the built-in methods for the rest, we maintain professionalism and keep our code clean and efficient. This approach ensures that we make the best use of the framework's tested and reliable functionality.
    """
    

"""
----> If we dont want to override the methods then we use directly inbuilt-methods.
"""
# Product List View : ListCreateAPIView
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}